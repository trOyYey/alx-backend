#!/usr/bin/env python3
""" 5-app task """

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Optional

class Config(object):
    """ class that contains babel config
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.route('/', strict_slashes=False)
def index():
    """ 6-app
    """
    return render_template('6-index.html')


@babel.localeselector
def get_locale() -> str:
    """
    get_local function to determine
    the best match with our supported languages
    """
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user.get('locale') in app.config["LANGUAGES"]:
        return g.user.get('locale')
    locale = request.headers.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Optional[dict]:
    """ function that defines the current user
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """ before_request """
    g.user = get_user()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
