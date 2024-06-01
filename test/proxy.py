import socket
import threading

servers = [
    ('localhost', 5001),
    ('localhost', 5002),
    ('localhost', 5003)
]

def FindFreeServer():
    for server in servers:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server)
            sock.sendall(b'STATUS')
            response = sock.recv(1024).decode()
            sock.close()
            if response == "FREE":
                return server
        except:
            continue
    
    return None

def handle_client(client_socket):
    server = FindFreeServer()
    if server:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(server)
        client_socket.sendall(f'REDIRECT {server[0]}:{server[1]}'.encode())
        print(f"[->] Redirected {client_socket} to {server}")
        client_socket.close()
    else:
        client_socket.sendall(b'NO AVAILABLE SERVERS')
        client_socket.close()

def proxy_server():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('0.0.0.0', 5000))
    proxy_socket.listen(5)
    print("[*] Proxy server is now listening on port 5000")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f'[*] Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    proxy_server()