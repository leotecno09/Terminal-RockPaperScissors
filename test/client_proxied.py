import socket

def connect_to_proxy(proxy_host, proxy_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.connect((proxy_host, proxy_port))
    
    # Riceve il messaggio di reindirizzamento dal proxy
    redirect_msg = proxy_socket.recv(1024).decode()
    proxy_socket.close()
    
    if redirect_msg.startswith('REDIRECT'):
        server_address = redirect_msg.split(' ')[1]
        server_host, server_port = server_address.split(':')
        return server_host, int(server_port)
    else:
        print("No available servers")
        return None, None

def connect_to_server(server_host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_host, server_port))
    return server_socket

def main():
    proxy_host = 'localhost'
    proxy_port = 5000
    
    server_host, server_port = connect_to_proxy(proxy_host, proxy_port)
    if server_host and server_port:
        server_socket = connect_to_server(server_host, server_port)
        
        try:
            while True:
                message = input("Enter message: ")
                if message.lower() == 'exit':
                    break
                
                server_socket.sendall(message.encode())
                response = server_socket.recv(1024).decode()
                print(f"Received from server: {response}")
        except KeyboardInterrupt:
            print("Client exiting...")
        finally:
            server_socket.close()

if __name__ == '__main__':
    main()
