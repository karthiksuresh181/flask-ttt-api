from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from functools import reduce

app = Flask(__name__)

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route('/', methods = ['POST', 'GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def index():
    if request.method == "POST":
        board = request.get_json()
        py_board = convert_py_board(board['board'])
        board = convert_back_board(py_board)
        for i in py_board:
            print(i)
        print(board)
        return jsonify("Post Method Call Success, {}".format(request.get_json()))
    else:
        return "Method Not Allowed"

if __name__ == '__main__':
    app.run()
