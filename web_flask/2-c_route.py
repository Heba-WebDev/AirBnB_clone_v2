#!/usr/bin/python3
""" C is fun! """
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def homepage():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_page():
    return "HBNB"

@app.route("/c/{value}", strict_slashes=False)
def c_page():
    return "C is {value}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
