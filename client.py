import socket
import os

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect
host = "127.0.0.1"
port = 5000
client_socket.connect((host, port))

clear_terminal()
nickname = input("Insert your nickname: ")
client_socket.sendall(nickname.encode("utf-8"))

while True:
    data = client_socket.recv(1024).decode("utf-8")
    print(data)

    if "Choose your move:" in data:
        move = input()
        client_socket.sendall(move.encode("utf-8"))



    