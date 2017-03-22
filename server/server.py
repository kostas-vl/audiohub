import os
import atexit
import sound
import drive.files
import settings.container as settings
import database.config as db
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


def main():
    # Flask App Initialization
    socketio.run(app, host=os.getenv('IP', '127.0.0.1'),
                 port=int(os.getenv('PORT', 5000)))

    emit('queue', playlist, broadcast=True)

    # settings.load()

    # db.init(settings.database_settings)


if __name__ == '__main__':
    main()
