"""
Contains constants for the flask and flask-socketio application runtime
"""
from flask import Flask
from flask_socketio import SocketIO

APP = Flask(__name__, static_url_path='/static')

SOCKET_IO = SocketIO(
    APP, 
    logger=True, 
    engineio_logger=True,
    cors_allowed_origins="*"
)
