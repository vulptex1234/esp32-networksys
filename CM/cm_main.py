import boot
import socket
import time
import _thread

s = None

def send():
    global s

    s = socket.socket()
    host = boot.wifi.ifconfig()[-1]
    PORT = 80

    try:
        s.connect(socket.getaddrinfo(host, PORT)[0][-1])
        print(f"Connected to {host}:{PORT}")
    except OSError as e:
        print(f"Failed to connect: {e}")
        s.close()
        return False
    return True

def send_to_server():
    if boot.connect_esp_wifi():
        print('Wi-Fi connected')
        time.sleep(5)
        if send():
            while True:
                # Node_ID, Battery, Nodesのペアを生成
                Node_ID = 2
                Battery = 90
                Nodes = [2, 3, 4]
                msg = f'{Node_ID},{Battery},"{" ".join(map(str, Nodes))}"'
                
                try:
                    s.sendall(msg.encode())
                    print(f"Sent: {msg}")
                except OSError as e:
                    print(f"Send failed: {e}")
                    s.close()
                    break
                time.sleep(30)
        else:
            print("Socket connection failed")
    else:
        print("Wi-Fi connection failed")

if __name__ == '__main__':
    _thread.start_new_thread(send_to_server,())