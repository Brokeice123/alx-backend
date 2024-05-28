#!/usr/bin/env python3
"""
Module that sets up a Flask App
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    Index route
    """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
