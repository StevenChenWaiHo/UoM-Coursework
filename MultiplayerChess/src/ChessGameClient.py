import socket, pickle, chess, re

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
GAMESTART_MESSAGE = "!GAMESTART"
GAMEEND_MESSAGE = "!GAMEEND"
SERVER = "192.168.1.112" # Change this to the server ip address
ADDR = (SERVER, PORT)

# Create socket object and connect it to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

moveRegEx = "^([a-h][1-8]){2}\Z"

# Send a message to server
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# Receive a message from server
def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
    return msg, client.recv(1).decode(FORMAT)

# Recieve board object from server
def receiveBoard():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
    return pickle.loads(msg)

gameStarted = False
message, response = receive()
while message != DISCONNECT_MESSAGE:
    print(message)
    # Prompt input log only when servser ask to response
    if int(response):
        message = input("Response: ")
        send(message)
    # Get repsonse from server
    message, response = receive()
    if message == GAMESTART_MESSAGE:
        gameStarted = True
    while gameStarted:
        # Get board from server
        board = receiveBoard()
        print(board)
        message, response = receive()
        # Quit game when server sent GAMEEND_MESSAGE
        if message == GAMEEND_MESSAGE:
            gameStarted = False
            message = "Game Ended"
            break;
        print(message)
        if int(response):
            # Ask for valid move
            move = input("Your Move: ")
            valid = re.search(moveRegEx, move)
            while not valid or chess.Move.from_uci(str(move)) not in board.legal_moves:
                move = input("Try again\nYour Move: ")
                valid = re.search(moveRegEx, move)
            send(move)


else:
    send(DISCONNECT_MESSAGE)
