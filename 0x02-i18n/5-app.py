#!/usr/bin/env python3
"""Module that sets up a Flask-Babel extension"""

from flask_babel import Babel
from flask import Flask, g, render_template, request

app = Flask(__name__)
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Configuration class for Flask app"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Set Babel's values using Config class to the flask app
app.config.from_object('3-app.Config')


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Default route for flask app"""
    return render_template('4-index.html')


@babel.localeselector
def get_locale() -> str:
    """Determine the best match for the supported languages"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        print(locale)
        return locale

    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id):
    """Retrieves user information from mock database
    Args:
        user_id (int): The ID of the user to retrieve.
    Returns:
        dict or None: The user dictionary if found, otherwise None """

    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """
    Retrieve user info before each request and set it as global variable.
    """
    user = get_user()
    g.user = user


if __name__ == "__main__":
    app.run(host="0.0.0.0")