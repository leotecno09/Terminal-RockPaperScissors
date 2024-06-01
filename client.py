import socket
import os
import sys
import time
import threading

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

def lobby():
    clear_terminal()

    print("Welcome to Terminal-RockPaperScissors! (Made by LeoTecno v1.0)")
    print("\nChoose an option:\n")
    print("1. Multiplayer")
    print("2. Quit")

    gamemode = input()
    gamemode = gamemode.upper()

    if gamemode == "1" or gamemode == "MULTIPLAYER":
        multiplayer()

    if gamemode == "2" or gamemode == "QUIT":
        print("Bye!")
        sys.exit(0)

    else:
        print("Please choose a vaild option.")
        time.sleep(3)
        lobby()

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

    server_address = str(input("Insert the server IP: "))               # DA METTERE CHE VADA ANCHE STRING
    server_port = int(input("Insert the server port (default 5000): "))

    if server_port == "":
        server_port = 5000

    host = server_address
    port = server_port

    try:
        client_socket.connect((host, port))

    except ConnectionRefusedError:
        print("[!] Error: Connection refused by the server.")
        print("[*] Back to the lobby...")
        time.sleep(5)
        lobby()

    except socket.gaierror:
        print("[!] Error: The IP address could not be found (socket.gaierror)")
        print("[*] Back to the lobby...")
        time.sleep(5)
        lobby()

    except TimeoutError:
        print("[!] Error: Unable to establish a connection with the server. (TimeoutError)")
        print("[*] Back to the lobby...")
        time.sleep(5)
        lobby()

    clear_terminal()
    print("[*] Connected!")

    nickname = input("Insert your nickname: ")
    client_socket.sendall(nickname.encode("utf-8"))

    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            print(data)

            if not data:
                print("[-] Disconnected from the server.")
                print("[*] Back to the lobby...")
                time.sleep(5)
                lobby()
                break

            if "Choose your move:" in data:
                move = input()
                client_socket.sendall(move.encode("utf-8"))

            if "Wanna play again?" in data:
                answer = input()
                client_socket.sendall(answer.encode("utf-8"))

            if "Nickname already in use" in data:
                nickname = input()
                client_socket.sendall(nickname.encode('utf-8'))

            if "Incorrect move" in data:
                move = input()
                client_socket.sendall(move.encode("utf-8"))

            if "Waiting for second player" in data:
                client_socket.sendall("alive".encode("utf-8"))

        except ConnectionAbortedError:
            print("[!] Error: Disconnected (ConnectionAbortedError)")
            print("[*] Back to the lobby...")
            time.sleep(5)
            lobby()
            break

        except ConnectionResetError:
            print("[!] Error: Disconnected (ConnectionResetError)")
            print("[*] Back to the lobby...")
            time.sleep(5)
            lobby()
            break

if __name__ == "__main__":
    lobby()
