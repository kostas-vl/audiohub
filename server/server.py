""" The initial file of the application """
import os
import settings.container as settings
import sound.player as player
import sound.playlist as playlist
import drive.files as files
import drive.file_system as file_system
import drive.download as download
from database.schema import DATABASE
from enviroment import SOCKET_IO, APP, emit, render_template


# Default http route
@APP.route('/')
def index():
    """ End point for the '/' path """
    return 'Audiohub API running...'


# New flask socket connection event handler
@SOCKET_IO.on('connect', namespace='/server')
def on_connect():
    """ function that handles a new connection socket """
    emit('my response', {'data': 'connected'})


# Flask socket disconnect event handler
@SOCKET_IO.on('disconnect', namespace='/server')
def on_disconnect():
    """ Function that handles a socket disconnect event """
    print('Client disconnected')


def main_operation(label, callback):
    """ Print a message on the console and executes the provide callback """
    print(label + '...')
    callback()


def main():
    """ The main source of the application execution """
    # Loading settings
    main_operation('Loading settings',
                   settings.load)
    # Initializing database
    main_operation('Initializing database schema image',
                   lambda: DATABASE.init(settings.DATABASE_SETTINGS))
    # Flask APP Initialization
    main_operation('Starting flask-SOCKET_IO server',
                   lambda: SOCKET_IO.run(
                       APP, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 5000))
                   ))
    emit('queue', playlist, broadcast=True)


if __name__ == '__main__':
    main()
