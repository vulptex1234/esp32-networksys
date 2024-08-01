import boot
import calc

import socket
import time
import _thread
import machine

PORT = 80
listen_socket = None
csv_file = 'node_data.csv'
param_dict = {}

# 期待されるクライアントの数を指定
expected_clients = 2
received_clients = []

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
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print('Close socket')
                conn.close()
                break
            decoded_data = data.decode()
            print('Received data:', decoded_data)
            
            # 受け取ったデータをCSVに格納
            node_data = parse_data(decoded_data)
            if node_data:
                update_csv(node_data)
                
                # クライアントの接続オブジェクトをトラッキング
                if conn not in received_clients:
                    received_clients.append(conn)
                
                # すべてのクライアントからデータを受信したか確認
                if len(received_clients) == expected_clients:
                    print('All clients data received. Processing...')
                    param_dict = calc.extract_from_csv()  # param_dictをcalc.extract_from_csvで更新
                    print('param_dict after extract_from_csv:', param_dict)  # 追加: param_dict の内容を確認
                    
                    cluster_head = calc.head_selection(param_dict)
                    for client in received_clients:
                        send_cluster_head(client, cluster_head)
                    
                    # 受信したクライアントリストをクリア
                    # received_clients = []
                    time.sleep(3)
                    machine.reset()

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
        nodes = int(parts[2].strip())  # ノードはスペース区切りのリストと仮定
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
            for line in lines[1:]:  # ヘッダー行をスキップ
                parts = line.strip().split(',')
                if len(parts) >= 3:  # 正しい形式の行だけを処理
                    node_id = int(parts[0].strip())
                    battery = int(parts[1].strip())
                    nodes = int(parts[2].strip())
                    data.append({"Node_ID": node_id, "Battery": battery, "Nodes": nodes})
    except OSError as e:
        print(f"Failed to read CSV: {e}")
    return data

def write_csv(file_path, data):
    try:
        with open(file_path, 'w') as file:
            file.write("Node_ID,Battery,Nodes\n")  # ヘッダーを書き込む
            for entry in data:
                file.write(f"{entry['Node_ID']},{entry['Battery']},{entry['Nodes']}\n")

        Data = []
        with open(file_path, 'r') as file:
            for l in file:
                l = l.rstrip(',')
                l = l.rstrip('\n')
                Data.append(l.split(','))
        print('CSV Data:', Data)  # 追加: CSVの内容を確認

    except OSError as e:
        print(f"Failed to write CSV: {e}")

def update_csv(new_data):
    global param_dict  # 追加: param_dict をグローバル変数として宣言
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
        msg = f"Cluster_Head,{cluster_head}"
        client.sendall(msg.encode())
        print(f"Sent cluster head info: {msg}")
        
    except OSError as e:
        print(f"Failed to send cluster head info: {e}")

if __name__ == '__main__':
    # boot.connect_home_wifi()
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