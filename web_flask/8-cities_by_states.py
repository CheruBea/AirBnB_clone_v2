#!/usr/bin/python3
"""
Starts a Flask web application
Route that lists cities by state
"""

from models import storage
from flask import Flask
from flask import render_template
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """List cities according to  given state"""
    s = storage.all(State)
    return render_template("8-cities_by_states.html", s=s)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
