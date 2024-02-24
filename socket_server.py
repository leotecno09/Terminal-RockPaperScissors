import socket
import threading
import time
import pickle

host = '127.0.0.1'
port = 5000
max_players = 2

players = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
print("[*] Listening on", port)

def handle_client(client_socket, client_address):
    print(f"[+] Player joined! {client_address}")

    #client_socket.sendall("Choose your nickname: ".encode('utf-8'))
    nickname = client_socket.recv(1024).decode('utf-8').strip()
    #print(nickname)

    players.append((client_socket, client_address, nickname))
    
    player_list = "\n".join([f"{i+1}. {player[2]}" for i, player in enumerate(players)]) # Senza ChatGPT non avrei saputo minimamente farlo
    broadcast("\nConnected players:\n" + player_list)

    #broadcast(f"Connected players: \n1. {}")

    if len(players) == max_players:
        #start_game()
        #start
        print("[*] Starting game!")

        broadcast("\n[+] Second player joined!")
        broadcast("\n[*] The game will start in 10 seconds...")

        time.sleep(10)
        start_game()
    
    else:
        broadcast("\n[*] Waiting for second player...")

def broadcast(message):
    for player in players:
        client_socket, client_address, nickname = player
        client_socket.sendall(message.encode("utf-8"))

def start_game():
    broadcast("[*] Starting!\n")

    while True:
        broadcast("Go for it! Choose your move: Rock (R), Paper (P) or Scissors (S)\n")
        moves = []
        for player in players:
            client_socket, client_address, nickname = player

            move = client_socket.recv(1024).decode("utf-8").strip().lower()
            move = move.upper()

            moves.append((nickname, move))

            if len(moves) == max_players:
                result = determineWinner(moves)
                broadcast(result)

def determineWinner(moves):                     # QUALCHE PROBLEMINO QUI...
    player1, move1 = moves[0]
    player2 , move2 = moves[1]

    print(player1)
    print(player2)

    print(move1)
    print(move2)

    if move1 == move2:
        return "It's a tie!"
    
    elif (move1 == 'ROCK' and move2 == 'SCISSORS') or \
         (move1 == 'PAPER' and move2 == 'ROCK') or \
         (move1 == 'SCISSOSRS' and move2 == 'PAPER'):
        return f"{player1} wins!"
    
   # elif (move2 == 'ROCK' and move1 == 'SCISSORS') or \
   #      (move2 == 'PAPER' and move1 == 'ROCK') or \
   #      (move2 == 'SCISSORS' and move1 == 'PAPER'):
   #     return f"{player2[2]} vince!"
    else:
        return f"{player2} wins!"



while True:
    client_socket, client_address = server.accept()

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()


