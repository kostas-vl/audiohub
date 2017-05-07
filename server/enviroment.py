""" Contains constants for the application runtime """
import pyglet
from flask import Flask
from flask_socketio import SocketIO, Namespace, emit

# Initializing the flask and flask-socketio apps
APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'secret!'
SOCKET_IO = SocketIO(APP)

# Pyglet configuration
pyglet.options['audio'] = ('openal', 'directsound')
