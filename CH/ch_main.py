import boot

import socket
import time
import _thread

PORT = 80
listen_socket = None

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
            print(data.decode())
        except OSError as e:
            print(f"Connection error: {e}")
            conn.close()
            break

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
