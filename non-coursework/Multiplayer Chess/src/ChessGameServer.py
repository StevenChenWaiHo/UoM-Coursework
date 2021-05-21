import socket
import threading
import chess
import pickle

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
GAMESTART_MESSAGE = "!GAMESTART"
GAMEEND_MESSAGE = "!GAMEEND"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

gameStarted = False

clients = []
playersReady = 0 # True when at least 1 player is ready

def handle_client(conn, addr):
    global gameStarted, playersReady, clients
    # Reject the 3rd player
    if threading.activeCount() - 1 > 2:
        send(conn, "Sorry there are 2 players already", False)
        send(conn, "You are disconnected from server", False)
        send(conn, "!DISCONNECT", False)
        print(f"[DECLINED PLAYER]  {addr} connection declined.")
        conn.close()
        return

    # Print player count and the address of the accepted client
    print(f"[NEW CONNECTION] {addr} connected.")
    print(f"[ACTIVE PLAYER] {threading.activeCount() - 1}")

    connected = True
    ready = False
    wait = False
    while connected:
        # Stop game when not enough players
        if threading.activeCount() - 1 == 1:
            gameStarted = False
            # Ask first player to wait for second player
            if conn not in clients:
                send(conn, "You are player 1. \nWaiting for second player", False)
                wait = True
                clients.append(conn)
            # Opponent left
            elif ready == True and wait == False:
                send(conn, "Opponent had left, You are player 1. \nWaiting for second player", False)
                wait = True

        # Add second player
        if threading.activeCount() - 1 == 2 and conn not in clients:
            send(conn, "You are player 2", False)
            clients.append(conn)

        # Init ready when the game started
        if gameStarted == True:
            ready = False

        # Ask to start game when theres 2 active clients
        if threading.activeCount() - 1 == 2 and ready == False and gameStarted == False:
            wait = False
            send(conn, "Start Game? (Y/!DISCONNECT)", True)
            message, connected = receive(conn)
            # Ask again for invalid answer
            while message != "Y" and connected:
                send(conn, "Try again. \nReady? (Y/!DISCONNECT)", True)
                message, connected = receive(conn)
            if not connected:
                clients.remove(conn)
                send(conn, "You are disconnected from server", False)
                conn.close()
                return
            ready = True
            playersReady += 1
            # Start game when both player ready (The second client start the game thread)
            if playersReady == 2:
                playersReady = 0
                gameStarted = True
                gameThread = threading.Thread(target=game, args=(clients,))
                gameThread.start()
            print(f"[{addr}] {message}")

    conn.close()


def start():
    server.listen()
    print(f"[HOST] Server is hosting on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def game(clients):
    global gameStarted
    board = chess.Board()
    for client in clients:
        send(client, GAMESTART_MESSAGE, False)
    turn = 0
    while gameStarted:
        sendBoard(clients, board)
        print(board)
        send(clients[turn], "Your Turn\n", True)
        send(clients[1 - turn], "Waiting Opponent Move\n", False)
        move, connected = receive(clients[turn])
        # Stop game when a player disconnect
        if connected == False:
            gameStarted = False
            sendBoard(clients, board)
            print(f"{clients[turn]} disconnected")
            for client in clients:
                send(client, GAMEEND_MESSAGE, False)
            send(clients[turn], "You are disconnected from server", False)
            send(clients[turn], "Opponent disconnected", False)
            clients.remove(clients[turn])
            clients[turn].close()
            return
        board.push(chess.Move.from_uci(str(move)))
        if board.is_game_over():
            sendBoard(clients, board)
            for client in clients:
                send(client, GAMEEND_MESSAGE, False)
                send(client, "You can start a new game", False)
            gameStarted = False
        turn = 1 - turn

# Send message to client and specified if repsonse needed
def send(conn, msg, rsp):
    if rsp:
        response = b'1'
    else:
        response = b'0'
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    conn.send(response)

# Send board to all players
def sendBoard(clients, board):
    board = pickle.dumps(board)
    msg_length = len(board)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    for client in clients:
        client.send(send_length)
        client.send(board)

def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            print(f"[PLAYER DISCONNECTED]")
            print(f"[ACTIVE PLAYER] {threading.activeCount() - 2}")
            return msg, False
        return msg, True


print("[STARTING] Server is starting...")
start()
