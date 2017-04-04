import os
import subprocess
import datetime
import sound.player as player
import sound.playlist as playlist
import drive.files as files
import drive.file_system as file_system
import drive.download as download
import settings.container as settings
import database.schema as db
from enviroment import *


# Default http route
@app.route('/')
def index():
    return 'Audiohub API running...'


# New flask socket connection event handler
@socketio.on('connect', namespace='/server')
def on_connect():
    emit('my response', {'data': 'connected'})


# Flask socket disconnect event handler
@socketio.on('disconnect', namespace='/server')
def on_disconnect():
    print('Client disconnected')


def main_operation(label, callback):
    print(label + '...')
    callback()


def main():
    # Loading settings
    main_operation('Loading settings', lambda: settings.load())

    # Initializing database
    main_operation('Initializing database schema image',
                   lambda: db.init(settings.database_settings))

    # Flask App Initialization
    main_operation('Starting flask-socketio server',
                   lambda: socketio.run(app,
                                        host=os.getenv('IP', '127.0.0.1'),
                                        port=int(os.getenv('PORT', 5000))))

    emit('queue', playlist, broadcast=True)


if __name__ == '__main__':
    main()
