# THIS IS A TEST

import socket
import select

HOST = '0.0.0.0'
PORT = 8888
BUFFER_SIZE = 4096

SERVERS = [
    {'address': ('127.0.0.1', 5000), 'max_clients': 2, 'current_clients': 0},
    {'address': ('127.0.0.1', 8002), 'max_clients': 2, 'current_clients': 0},
    {'address': ('127.0.0.1', 8003), 'max_clients': 2, 'current_clients': 0}
]

def get_server():
    global SERVERS
    for server in SERVERS:
        if server['current_clients'] < server['max_clients']:
            return server['address']
    
    return None


def start_proxy():
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_server.bind((HOST, PORT))
    proxy_server.listen(10)

    print(f"[*] Proxy listening on {HOST}:{PORT}")

    inputs = [proxy_server]

    while True:
        readable, _, _ = select.select(inputs, [], [])

        for sock in readable:
            if sock == proxy_server:
                client_socket, client_address = proxy_server.accept()
                print(f"[+] Connection from {client_address}")

                server_address = get_server()
                if server_address:
                    print(f"[->] Sending to {server_address}")

                    game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    game_server.connect(server_address)

                    client_socket.sendall(b"Connection succeeded\n")
                    game_server.sendall(b"Connection succeeded\n")

                    for server in SERVERS:
                        if server['address'] == server_address:
                            server['current_clients'] += 1
                            break
                
                else:
                    print("[!] No server found!")
                    client_socket.sendall(b"[!] No server found! Retry later.")
                    client_socket.close()

if __name__ == "__main__":
    start_proxy()