from flask import Flask
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        return "Post Method Call Success"
    else:
        return "Get Method Call Success"

if __name__ == '__main__':
    app.run()
