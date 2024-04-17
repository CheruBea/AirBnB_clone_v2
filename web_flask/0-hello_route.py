#!/usr/bin/python3
"""
Starts a Flask web application
Listening on 0.0.0.0 and port 5000
"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_HBNB():
    """Displays hello HBNB!"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
