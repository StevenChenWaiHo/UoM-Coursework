import chess

board = chess.Board()
print(board)
inputMove = input("Move: ")
while inputMove != "!DISCONNECT" and not board.is_game_over():
    inputMove = chess.Move.from_uci(str(inputMove))
    if inputMove in board.legal_moves:
        board.push(chess.Move.from_uci(str(inputMove)))
        print(board)
        print()
    else:
        print("Illegal Move")
    inputMove = input("Move: ")
