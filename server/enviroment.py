"""
Contains constants for the application runtime
"""
from flask import Flask
from flask_socketio import SocketIO

# Initializing the flask and flask-socketio apps
APP = Flask(__name__, static_url_path='/static')
APP.config['SECRET_KEY'] = 'secret!'
SOCKET_IO = SocketIO(APP)
