from flask import Flask, request
app = Flask(__name__)
import os

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    return "Hello %s from %s in check app." % (path , os.popen("hostname").read())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8083)
