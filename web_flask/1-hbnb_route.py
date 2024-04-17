#!/usr/bin/python3
"""
Starts a flask web application
listens on port 5000, on any host 0.0.0.0
Two routes involved
"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_HBNB():
    """Displays Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def HBNB():
    """Displays HBNB"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
