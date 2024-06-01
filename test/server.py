import socket
import threading

server_state = {
    'status': 'FREE'
}

def handle_client(client_socket):
    global server_state
    server_state['status'] = 'BUSY'
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # Gestisci i dati ricevuti
        client_socket.sendall(b'ECHO: ' + data)
    client_socket.close()
    server_state['status'] = 'FREE'

def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f'Server listening on port {port}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr}')
        if server_state['status'] == 'FREE':
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        else:
            client_socket.sendall(b'SERVER BUSY')
            client_socket.close()

def status_listener(port):
    status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status_socket.bind(('0.0.0.0', port + 10000))
    status_socket.listen(1)
    print(f'Status listener on port {port + 10000}')

    while True:
        status_client, addr = status_socket.accept()
        data = status_client.recv(1024)
        if data == b'STATUS':
            status_client.sendall(server_state['status'].encode())
        status_client.close()

if __name__ == '__main__':
    import sys

    port = int(sys.argv[1])  # Passa la porta come argomento
    threading.Thread(target=status_listener, args=(port,)).start()
    server(port)
