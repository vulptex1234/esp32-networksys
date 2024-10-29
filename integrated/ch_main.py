
import boot
import calc
import socket
import time
import _thread
import machine
from get_current import remaining_battery_percentage
from boot import connected_nodes, expected_clients

PORT = 80
listen_socket = None
csv_file = 'node_data.csv'
param_dict = {}
with open('ID.txt', 'r') as file:
    Node_ID = int(file.readline().strip())

# expected_clients = 4
received_clients = []
# connected_nodes = 3 

def start_server():
    global listen_socket
    ip = boot.ap.ifconfig()[0]
    listen_socket = socket.socket()
    listen_socket.bind((ip, PORT))
    listen_socket.listen(5)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Server started at {ip}:{PORT}")

def handle_client(conn, addr):
    global param_dict, received_clients
    print('Connected from: ', addr)

    # 自ノードのデータを準備
    own_node_data = {
        "Node_ID": Node_ID,
        "Battery": int(remaining_battery_percentage),  # バッテリー残量を整数に変換
        "Nodes": connected_nodes
    }

    # CSVファイルに自ノードのデータを追加
    update_csv(own_node_data)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print('Close socket')
                conn.close()
                break
            decoded_data = data.decode()
            print('Received data:', decoded_data)
            
            node_data = parse_data(decoded_data)
            if node_data:
                update_csv(node_data)

                if conn not in received_clients:
                    received_clients.append(conn)
                
                if len(received_clients) == expected_clients:
                    print('All clients data received. Processing...')
                    try:
                        param_dict = calc.extract_from_csv_norm()
                        print('param_dict after extract_from_csv_norm:', param_dict)

                        # cluster_head = calc.leach(param_dict) #leachの時
                        cluster_head = calc.head_selection(param_dict)
                        # cluster_head_ID = cluster_head[0] #leachの時
                        cluster_head_ID = cluster_head

                        
                        for client in received_clients:
                            send_cluster_head(client, cluster_head)

                        received_clients = []
                        time.sleep(3)

                        if cluster_head_ID == Node_ID:
                            new_flag = 'True'
                        else:
                            new_flag = 'False'
                        with open('flag.txt', 'w') as file:
                            file.write(new_flag)

                        boot.p2.off()
                        machine.reset()

                    except ValueError as ve:
                        print(f"Error processing CSV data: {ve}")
        except OSError as e:
            print(f"Connection error: {e}")
            conn.close()
            break

def parse_data(data):
    try:
        parts = data.split(',')
        node_id = int(parts[0].strip())
        battery = int(parts[1].strip())
        nodes = int(parts[2].strip())
        return {"Node_ID": node_id, "Battery": battery, "Nodes": nodes}
    except Exception as e:
        print(f"Failed to parse data: {e}")
        return None

def file_exists(file_path):
    try:
        with open(file_path, 'r'):
            pass
        return True
    except OSError:
        return False

def read_csv(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    try:
                        node_id = int(parts[0].strip())
                        battery = int(parts[1].strip())
                        nodes = int(parts[2].strip())
                        data.append({"Node_ID": node_id, "Battery": battery, "Nodes": nodes})
                    except ValueError as ve:
                        print(f"ValueError: {ve} for line: {line.strip()}")
    except OSError as e:
        print(f"Failed to read CSV: {e}")
    return data

def write_csv(file_path, data):
    try:
        with open(file_path, 'w') as file:
            file.write("Node_ID,Battery,Nodes\n")
            for entry in data:
                file.write(f"{entry['Node_ID']},{entry['Battery']},{entry['Nodes']}\n")

        Data = []
        with open(file_path, 'r') as file:
            for l in file:
                l = l.rstrip(',')
                l = l.rstrip('\n')
                Data.append(l.split(','))
        print('CSV Data:', Data)

    except OSError as e:
        print(f"Failed to write CSV: {e}")

def update_csv(new_data):
    global param_dict
    if file_exists(csv_file):
        data = read_csv(csv_file)
        updated = False
        for entry in data:
            if entry["Node_ID"] == new_data["Node_ID"]:
                entry["Battery"] = new_data["Battery"]
                entry["Nodes"] = new_data["Nodes"]
                updated = True
                break
        if not updated:
            data.append(new_data)
    else:
        data = [new_data]
    
    write_csv(csv_file, data)

def send_cluster_head(client, cluster_head):
    try:
        msg = f"{cluster_head}"
        client.sendall(msg.encode())
        print(f"Sent cluster head info: {msg}")
        
    except OSError as e:
        print(f"Failed to send cluster head info: {e}")

if __name__ == '__main__':
    boot.ap_activate()

    start_server()

    while True:
        print('Accepting......')
        try:
            conn, addr = listen_socket.accept()
            _thread.start_new_thread(handle_client, (conn, addr))
            
        except OSError as e:
            print(f"Accept error: {e}")
            continue
        time.sleep(1)

