import boot
import socket
import time
import _thread
import random
import machine
from get_current import remaining_battery_percentage
from boot import connected_nodes

s = None

# Wi-Fi接続をトライし続ける関数
def connect_wifi():
    while not boot.connect_esp_wifi():
        print("Wi-Fi connection failed, retrying...")
        time.sleep(5)  # 再試行までの待機時間
    print("Wi-Fi connected")
    return True

# サーバーへの接続をトライし続ける関数
def send():
    global s

    while True:
        try:
            s = socket.socket()
            host = boot.wifi.ifconfig()[-1]
            PORT = 80
            s.connect(socket.getaddrinfo(host, PORT)[0][-1])
            print(f"Connected to {host}:{PORT}")
            return True
        except OSError as e:
            print(f"Failed to connect to server: {e}. Retrying...")
            s.close()
            time.sleep(5)  # 再試行までの待機時間

# メインのデータ送信関数
def send_to_server():
    # Wi-Fi接続を確立するまで繰り返す
    connect_wifi()

    time.sleep(5)  # 接続後に少し待機
    # サーバー接続を確立するまで繰り返す
    if send():
        while True:
            # Node_ID, Battery, Nodesのペアを生成
            with open('ID.txt', 'r') as file:
                Node_ID = int(file.readline())
            Battery = int(remaining_battery_percentage)
            msg = f'{Node_ID},{Battery},{connected_nodes}'
            
            try:
                s.sendall(msg.encode())
                print(f"Sent: {msg}")
                
                # サーバーからの応答を待つ
                response = s.recv(1024)
                if response:
                    response_decoded = response.decode().strip()
                    print(f"Received: {response_decoded}")

                    # 応答メッセージのパース
                    response_parts = response_decoded.strip("()").split(",")
                    try:
                        received_node_id = int(response_parts[0].strip())
                    except ValueError as e:
                        print(f"Error parsing node ID: {e}")
                        received_node_id = None
            except OSError as e:
                print(f"Send/Receive failed: {e}")
                s.close()
                break

            time.sleep(3)
            
            # Flag処理(Test)
            if received_node_id == Node_ID:
                new_flag = 'True'
            else:
                new_flag = 'False'
            
            with open('flag.txt', 'w') as file:
                file.write(new_flag)
            
            boot.p2.off()
            machine.reset()

    boot.p2.off()

if __name__ == '__main__':
    _thread.start_new_thread(send_to_server, ())