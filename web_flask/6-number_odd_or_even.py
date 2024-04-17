#!/usr/bin/python3
"""
Starting a web application
listeoning on 0.0.0.0 through port 5000
"""


from flask import Flask, render_template

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
    """an int variable"""
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def render_html(n):
    """rendering a html page"""
    return render_template("5-number.html", n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def render_html_oddor_even(n):
    """introduce or in the template rendered"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
