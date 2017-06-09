""" The initial file of the application """
import os
import settings.container as settings
import sound.player as player
import sound.playlist as playlist
import drive.files as files
import drive.file_system as file_system
import drive.download as download
from database.schema import DATABASE
from enviroment import SOCKET_IO, APP, emit


# Default http route
@APP.route('/')
def index():
    """ End point for the '/' path """
    return 'Audiohub API running...'


# New flask socket connection event handler
@SOCKET_IO.on('connect', namespace='/server')
def on_connect():
    """ function that handles a new connection socket """
    print('Client connected')


# Flask socket disconnect event handler
@SOCKET_IO.on('disconnect', namespace='/server')
def on_disconnect():
    """ Function that handles a socket disconnect event """
    print('Client disconnected')


def main():
    """ The main source of the application execution """
    # Loading settings
    print("Loading settings...")
    settings.load()
    # Initializing database
    print("Initializing database schema image...")
    DATABASE.init(settings.DATABASE)
    # Flask APP Initialization
    print("Starting the flask socket-io server...")
    SOCKET_IO.run(
        APP,
        host=os.getenv('IP', settings.SERVER['ip']),
        port=int(os.getenv('PORT', 5000))
    )
    # Send out the current playlist
    emit('queue', playlist, broadcast=True)


if __name__ == '__main__':
    main()
