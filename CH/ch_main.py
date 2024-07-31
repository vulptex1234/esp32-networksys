import boot
import socket
import time
import _thread

PORT = 80
listen_socket = None
csv_file = 'node_data.csv'

def start_server():
    global listen_socket
    ip = boot.ap.ifconfig()[0]
    listen_socket = socket.socket()
    listen_socket.bind((ip, PORT))
    listen_socket.listen(5)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Server started at {ip}:{PORT}")

def handle_client(conn, addr):
    print('connected from: ', addr)
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print('close socket')
                conn.close()
                break
            decoded_data = data.decode()
            print(decoded_data)
            
            # 受け取ったデータをCSVに格納
            node_data = parse_data(decoded_data)
            if node_data:
                save_to_csv(node_data)
                
        except OSError as e:
            print(f"Connection error: {e}")
            conn.close()
            break

def parse_data(data):
    try:
        # データは"Node_ID,Battery,Nodes"のフォーマットで送信されると仮定
        parts = data.split(',')
        node_id = int(parts[0].strip())
        battery = int(parts[1].strip())
        nodes = parts[2].strip().split()  # ノードはスペース区切りのリストと仮定
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

def save_to_csv(node_data):
    file_exists_flag = file_exists(csv_file)
    with open(csv_file, mode='a') as file:
        if not file_exists_flag:
            file.write("Node_ID,Battery,Nodes\n")  # ヘッダーを書き込む
        file.write(f"{node_data['Node_ID']},{node_data['Battery']},{' '.join(node_data['Nodes'])}\n")

    Data = []
    with open(csv_file, mode='r') as file:
        for l in file:
            l = l.rstrip(',')
            l = l.rstrip('\n')
            Data.append(l.split(','))
    print(Data)

if __name__ == '__main__':
    # boot.connect_home_wifi()
    boot.ap_activate()
    start_server()

    while True:
        print('accepting......')
        try:
            conn, addr = listen_socket.accept()
            _thread.start_new_thread(handle_client, (conn, addr))
        except OSError as e:
            print(f"Accept error: {e}")
            continue
        time.sleep(1)