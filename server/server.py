import os
import atexit
import samba
import player
import files
import config
from enviroment import *
from config import *


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
    config.load_queries()

    

    # socketio.run(app, host=os.getenv('IP', '127.0.0.1'),
    #              port=int(os.getenv('PORT', 5000)))

    # emit('queue', playlist, broadcast=True)

    # atexit.register(config.update)


if __name__ == '__main__':
    main()
