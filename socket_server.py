import socket
import threading
import time
import win32api

def read_config(key, filename="config.cfg"):
    with open(filename, "r") as file:
        for line in file:
            if line.startswith(key):
                value = line.split("=")[1].strip()

                try:
                    value = int(value)
                
                except ValueError:
                    pass

                return value
        
    return f"{key} not found in 'config.cfg'"


host = read_config("IP")
port = read_config("PORT")

max_players = 2

players = []

player1_points = 0
player2_points = 0
tie = 0

threadsRunning = True
game_started = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
print("[*] Listening on", port)

def close_server(signal_type):
    confirm = str(input("[*] Are you sure you want to close the server? (y/n) "))
    confirm = confirm.upper()

    if confirm == "Y":
        print("[*] Closing!")
        server.close()
        time.sleep(5)
        exit()
        #break
        
    else:
        print("[*] Nothing changed, i'm still running!")

win32api.SetConsoleCtrlHandler(close_server, True)

def handle_client(client_socket, client_address):
    try:
        nickname = client_socket.recv(1024).decode('utf-8').strip()
    
    except (ConnectionAbortedError, ConnectionResetError) as e:
        print(f"[!] Client lost connection: {client_address} ({e})")
        for player in players:
            if player[:2] == (client_socket, client_address):
                players.remove(player)
                break

            client_socket.close()
            print(players)
            print(client_socket)
        
    while any(player[2] == nickname for player in players):
        client_socket.send("Nickname already in use. Please choose a different one:".encode("utf-8"))
        nickname = client_socket.recv(1024).decode('utf-8').strip()
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
        broadcast("\n[*] Waiting for second player...") # SE UN CLIENT SI DISCONNETTE QUI, IL SERVER NON LO RILEVA!               
        try:
            client_status = client_socket.recv(1024).decode('utf-8').strip()
            print(client_status)

        except ConnectionResetError as e:
            print(f"[!] Client lost connection: {client_address} ({e})")            # ho tolto "while not game_started" e non va più un caz, da rivedereeee
            for player in players:
                if player[:2] == (client_socket, client_address):
                    players.remove(player)
                    break

                client_socket.close()
                print(players)
                print(client_socket)              
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
    game_started = True
    global player1_points
    global player2_points
    global tie

    player1_points = 0
    player2_points = 0
    tie = 0

    rounds = read_config("ROUNDS")
    print("[*] Number of rounds: ", rounds)

    #rounds = 3

    broadcast("\n[*] The game will start in 10 seconds...")
    time.sleep(10)

    broadcast("[*] Starting!\n")

    try:
        for x in range(rounds):
            broadcast("Go for it! Choose your move: Rock (R), Paper (P) or Scissors (S)\n")
            moves = []
            for player in players:
                client_socket, client_address, nickname = player

                move = client_socket.recv(1024).decode("utf-8").strip().lower()
                move = move.upper()

                while move not in ['ROCK', 'PAPER', 'SCISSORS', 'R', 'P', 'S']:                                     # non funziona molto bene
                    client_socket.send("Incorrect move, please type Rock, Paper or Scissors.\n".encode("utf-8"))
                    move = client_socket.recv(1024).decode("utf-8").strip().lower()
                    move = move.upper()

                moves.append((nickname, move))

                if len(moves) == max_players:
                    result = determineWinner(moves)
                    broadcast(result)
        
    except ConnectionResetError:
        print(f"[!] Client lost connection during a game: {client_address}")
        print(client_socket)
        players.remove((client_socket, client_address, nickname))
        client_socket.close()
        broadcast("\n[!] A client disconnected from the server. This game is over, resetting the server.")
        resetServer()

    broadcast("\n[*] End!\n")
    stopGame(moves)

"""def checkPlayerConnection():
        disconnected_players = []

        for client_socket, client_address, nickname in players:
            try:
                client_socket.sendall(b"")
                print("Pinging clients.")

            except ConnectionError:
                print(f"[!] Player {client_address} disconnected unexpectedly. Game over.")
                disconnected_players.append((client_socket, client_address, nickname))

            
            for disconnected_player in disconnected_players:
                players.remove(disconnected_player)

            if disconnected_players:
                broadcast("\n[!] A client disconnected from the server. This game is over, resetting the server.")
                time.sleep(2)
                resetServer()

        time.sleep(1)"""         

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
    if move1 == "ROCK" and move2 == "PAPER" or move1 == "R" and move2 == "P":
        player2_points += 1
        return f"\n{player2} wins!\n"
    
    if move1 == "PAPER" and move2 == "SCISSORS" or move1 == "P" and move2 == "S":
        player2_points += 1
        return f"\n{player2} wins!\n"
    
    if move1 == "SCISSORS" and move2 == "ROCK" or move1 == "S" and move2 == "R":
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
            if answers[0] == "Y" and answers[1] == "Y":
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
    global threadsRunning

    print("[*] Resetting the server, disconnecting players.")

    for player in players:
        client_socket, _, _ = player
        client_socket.close()

    players = []
    player1_points = 0
    player2_points = 0
    tie = 0

    threadsRunning = False                  # DA IMPLEMENTARE SE POSSIBILE

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
        #threading.Thread(target=checkPlayerConnection, daemon=True).start()
        client_thread.start()

    else:
        client_socket.close()

