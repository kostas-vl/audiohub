import os
import atexit
import datetime
import sound.player as player
import sound.playlist as playlist
import drive.files as files
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


def main():
    # Flask App Initialization
    # socketio.run(app, host=os.getenv('IP', '127.0.0.1'),
    #              port=int(os.getenv('PORT', 5000)))

    # emit('queue', playlist, broadcast=True)

    settings.load()

    db.init(settings.database_settings)

    # playlist.insert(playlist.Playlist({
    #     'id': 1,
    #     'name': 'FinalFantasyMainTheme.mp3',
    #     'type': 'file',
    #     'path': 'C:/Users/kvl_9/Music/fantasy.mp3',
    #     'active': True,
    #     'date_created': datetime.datetime.now(),
    #     'date_modified': datetime.datetime.now()
    # }))

    print(playlist.selectActive())


if __name__ == '__main__':
    main()
