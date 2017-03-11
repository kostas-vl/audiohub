import sys
import pyglet
from flask import Flask
from flask_socketio import SocketIO, Namespace, emit

# Initializing the flask and flask-socketio apps
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Pyglet configuration
pyglet.options['audio'] = ('openal', 'directsound')
