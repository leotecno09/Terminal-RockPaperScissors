import socket
import os
import time

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

def lobby():
    clear_terminal()

    print("Welcome to Terminal-RockPaperScissors!")
    print("\nChoose an option:\n")
    print("1. Multiplayer")
    print("2. Quit")

    gamemode = input()
    gamemode = gamemode.upper()

    if gamemode == "1" or gamemode == "MULTIPLAYER":
        multiplayer()

def multiplayer():
    '''while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            server_address = input("Insert the server IP: ")
            server_port = input("Insert the server port (default 5000): ")

            if server_port == "":
                server_port = 5000
            
            host = server_address
            port = server_port
            client_socket.connect((host, port))

            clear_terminal()
            print("[*] Connected!")
            
            connected = True

            nickname = input("Insert your nickname: ")
            client_socket.sendall(nickname.encode("utf-8"))

            while connected:
                data = client_socket.recv(1024).decode("utf-8")

                print(data)

                if "Choose your move:" in data:
                    move = input()
                    client_socket.sendall(move.encode("utf-8"))
                    
                if "Wanna play again?" in data:
                    answer = input()
                    client_socket.sendall(answer.encode("utf-8"))

        except ConnectionResetError:
            print("[*] Disconnected. (ConnectionReset)")
            connected = False
            print("[*] Back to the lobby...")
            time.sleep(3)
            lobby()

        except Exception as e:
            print(f"[!] An error occurred: {e}")
            
        finally:
            client_socket.close()

            print("[*] Back to the lobby...")
            time.sleep(3)
            lobby()'''
    


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = input("Insert the server IP: ")
    server_port = input("Insert the server port (default 5000): ")

    if server_port == "":
        server_port = 5000
            
    host = server_address
    port = server_port
    client_socket.connect((host, port))

    clear_terminal()
    print("[*] Connected!")

    nickname = input("Insert your nickname: ")
    client_socket.sendall(nickname.encode("utf-8"))

    while True:
        data = client_socket.recv(1024).decode("utf-8")
        print(data)

        if "Choose your move:" in data:
            move = input()
            client_socket.sendall(move.encode("utf-8"))

        if "Wanna play again?" in data:
            answer = input()
            client_socket.sendall(answer.encode("utf-8"))


if __name__ == "__main__":
    lobby()