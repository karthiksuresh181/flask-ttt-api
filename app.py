from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from functools import reduce
import numpy as np
import random
from keras.models import load_model

app = Flask(__name__)

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i, j))
    return moves

def bestMove(board, model, player, rnd=0):
    scores = []
    moves = getMoves(board)
    
    # Make predictions for each possible move
    for i in range(len(moves)):
        future = np.array(board)
        future[moves[i][0]][moves[i][1]] = player
        prediction = model.predict(future.reshape((-1, 9)))[0]
        if player == 1:
            winPrediction = prediction[1]
            lossPrediction = prediction[2]
        else:
            winPrediction = prediction[2]
            lossPrediction = prediction[1]
        drawPrediction = prediction[0]
        if winPrediction - lossPrediction > 0:
            scores.append(winPrediction - lossPrediction)
        else:
            scores.append(drawPrediction - lossPrediction)

    # Choose the best move with a random factor
    bestMoves = np.flip(np.argsort(scores))
    for i in range(len(bestMoves)):
        if random.random() * rnd < 0.5:
            return moves[bestMoves[i]]


    # Choose a move completely at random
    return moves[random.randint(0, len(moves) - 1)]

def convert_py_board(board):
    for i in range(len(board)):
        if board[i] == 'none':
            board[i] = 0
        elif board[i] == 'X':
            board[i] = 1
        else:
            board[i] = 2
    py_board = []
    py_board.append(board[:3])
    py_board.append(board[3:6])
    py_board.append(board[6:9])
    return py_board

def convert_back_board(board):
    board = reduce(lambda x,y: x+y, board)
    for i in range(len(board)):
        if board[i] == 0:
            board[i] = 'none'
        elif board[i] == 1:
            board[i] = 'X'
        else:
            board[i] = 'O'
    return board

def something(board, playerToMove):
    model = load_model("tictactoe.h5")
    move = bestMove(board, model, playerToMove, 0)
    board[move[0]][move[1]] = playerToMove
    return board, "{}{}".format(move[0], move[1])

@app.route('/', methods = ['POST', 'GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def index():
    if request.method == "POST":
        board = request.get_json()
        py_board = convert_py_board(board['board'])
        py_board, index = something(py_board, 2)
        board = convert_back_board(py_board)
        return jsonify(board, index)
    else:
        return "Method Not Allowed"

if __name__ == '__main__':
    app.run(threaded=False)
