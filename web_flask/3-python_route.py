#!/usr/bin/python3
""" Python is cool! """
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def homepage():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_page():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_page(text):
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route("/python/<text>", strict_slashes=False)
def python_page(text):
    text = text.replace('_', ' ')
    return "C {}".format(text)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
