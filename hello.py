from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        return "Post Method Call Success, {}".format(request.get_json())
    else:
        return "Get Method Call Success"

if __name__ == '__main__':
    app.run()
