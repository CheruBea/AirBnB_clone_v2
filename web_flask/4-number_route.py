#!/usr/bin/python3
"""
Starting a web application
listeoning on 0.0.0.0 through port 5000
"""


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display Hello HBNB"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def route_with_var(text="is cool"):
    """A route with a variable"""
    text = text.replace("_", " ")
    return f"C {text}"


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def route1_with_var(text="is cool"):
    """Another route with a variable"""
    text = text.replace("_", " ")
    return f"Python {text}"


@app.route('/number/<int:n>', strict_slashes=False)
def interger_route(n):
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
