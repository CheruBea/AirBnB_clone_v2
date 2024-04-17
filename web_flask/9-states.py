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


@app.route('/states', strict_slashes=False)
def states():
    """List cities according to  given state"""
    states = storage.all(State)
    return render_template("9-states.html", state=states)


@app.route('/states/<id>', strict_slashes=False)
def states_with_id(id):
    """
    States with specific id and their cities
    The .values() method is used to obtain a collection of
    all state objects"""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
