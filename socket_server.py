import socket
import threading
import time
import win32api
import sys

host = '0.0.0.0'
port = 5000
max_players = 2

players = []

player1_points = 0
player2_points = 0
tie = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
print("[*] Listening on", port)

def close_server(signal_type):
    confirm = str(input("[*] Are you sure you want to close the server? (y/n) "))
    confirm = confirm.upper()

    if confirm == "Y":
        print("[*] Closing!")
        sys.exit(0)
        #break
        
    else:
        print("[*] Nothing changed, i'm still running!")

win32api.SetConsoleCtrlHandler(close_server, True)

def handle_client(client_socket, client_address):
    try:
        nickname = client_socket.recv(1024).decode('utf-8').strip()

        for player in players:                          # ovviamente non funziona, da ricontrollare
            if player[2] == nickname:
                print(f"[-] Connection from {client_address} refused. Nickname already exists.")
                client_socket.close()
            #print(nickname)

        print(f"[+] Player joined! {client_address}")
        players.append((client_socket, client_address, nickname))
            
        player_list = "\n".join([f"{i+1}. {player[2]}" for i, player in enumerate(players)]) # Senza ChatGPT non avrei saputo minimamente farlo
        broadcast("\nConnected players:\n" + player_list)

            #broadcast(f"Connected players: \n1. {}")

        if len(players) == max_players:
            #start_game()
            #start
            print("[*] Starting game!")

            broadcast("\n[+] Second player joined!")
            start_game()
            
        else:
            broadcast("\n[*] Waiting for second player...")
    
    except ConnectionAbortedError or ConnectionResetError:
        print(f"[!] Client lost connection: {client_address}")
        players.remove((client_socket, client_address, nickname))
        client_socket.close()
        print(players)
        print(client_socket)

    #except ConnectionAbortedError:
    #    print(f"[!] Connection lost with {client_address}")
    #    return
    #
    #finally:
    #    if nickname:
    #        players.remove((client_socket, client_address, nickname))
    #    client_socket.close()

def broadcast(message):
    for player in players:
        client_socket, client_address, nickname = player
        client_socket.sendall(message.encode("utf-8"))

def start_game():
    global player1_points
    global player2_points
    global tie

    player1_points = 0
    player2_points = 0
    tie = 0

    broadcast("\n[*] The game will start in 10 seconds...")
    time.sleep(10)

    broadcast("[*] Starting!\n")

    try:
        for x in range(3):
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
        
    except ConnectionResetError:
        print(f"[!] Client lost connection during a game: {client_address}")
        players.remove((client_socket, client_address, nickname))
        client_socket.close()
        broadcast("\n[!] A client disconnected from the server. This game is over, resetting the server.")
        resetServer()

    broadcast("\n[*] End!\n")
    stopGame(moves)

def determineWinner(moves):
    #print (moves)

    global player1_points
    global player2_points
    global tie

    player1, move1 = moves[0]
    player2 , move2 = moves[1]

    #print(player1)
    #print(player2)

    #print(move1)
    #print(move2)

    if move1 == move2:
        tie += 1
        return "\nIt's a tie!\n"
    
    # Sequenza uno ad uno perchè si --- da mettere che legge anche sole lettere
    if move1 == "ROCK" and move2 == "PAPER":
        player2_points += 1
        return f"\n{player2} wins!\n"
    
    if move1 == "PAPER" and move2 == "SCISSORS":
        player2_points += 1
        return f"\n{player2} wins!\n"
    
    if move1 == "SCISSORS" and move2 == "ROCK":
        player2_points += 1
        return f"\n{player2} wins!\n"
    
    else:
        player1_points += 1
        return f"\n{player1} wins!\n"

def stopGame(moves):  
    player1, move1 = moves[0]   # move1 e move2 sono inutili, ricicliamo variabili :)
    player2, move2 = moves[1]

    global player1_points
    global player2_points
    global tie

    broadcast(f"\nScore:\n\n")
    broadcast(f"{player1}: {player1_points}\n{player2}: {player2_points}\nTie: {tie}")

    if player1_points > player2_points:
        broadcast(f"\n\n{player1} is the winner of this game!")
    
    if player1_points < player2_points:
        broadcast(f"\n\n{player2} is the winner of this game!")

    if player1_points == player2_points:
        broadcast(f"\n\n...and it's a tie!")

    playAgain()

def playAgain():
    broadcast("\n\nWanna play again? [y/n]")

    answers = []
    for player in players:
        client_socket, _, _ = player

        answer = client_socket.recv(1024).decode("utf-8").strip().lower()
        answer = answer.upper()

        answers.append((answer))

        if len(answers) == max_players:
            if answers[0] == "y" and answers[1] == "y":
                broadcast("Two players wants to play again!")
                start_game()
          
            else:
                broadcast("A player doesn't want to play again, the server will restart. Goodbye!")
                resetServer()

def resetServer():
    global players
    global player1_points
    global player2_points
    global tie

    print("[*] Resetting the server, disconnecting players.")

    for player in players:
        client_socket, _, _ = player
        client_socket.close()

    players = []
    player1_points = 0
    player2_points = 0
    tie = 0

    print("[*] Server resetted, ready for a new game.")

def refuseClient(client_address):
    if len(players) >= 2:
        print(f"[-] Connection from {client_address} refused. Too many players!")
        return False
    
    return True

while True:
    client_socket, client_address = server.accept()

    if refuseClient(client_address):
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

    else:
        client_socket.close()

