""" The initial file of the application """
import os
import settings.container as settings
import models.users as usr
import models.user_settings as stt
import models.file_system
import models.playlist
import sound.player as player
import drive.files as files
import drive.download as download
from flask import request, send_from_directory
from flask_socketio import join_room, leave_room
from database.schema import DATABASE
from enviroment import SOCKET_IO, APP, emit


# Default http route
@APP.route('/')
def on_index():
    """ End point for the '/' path """
    return send_from_directory('static', 'index.html')


@APP.route('/<path:path>')
def on_static_file(path):
    """ Serve any static file  """
    return send_from_directory('static', path)


# New flask socket connection event handler
@SOCKET_IO.on('connect', namespace='/server')
def on_connect():
    """ function that handles a new connection socket """
    try:
        users = usr.select_by_ip(request.host)
        if users:
            # Loop through the users and update them
            for user in users:
                user.session_id = request.sid
                user.active = True
                user_settings = stt.select_by_user_id(user.identity)
                if user_settings:
                    user.settings = user_settings[0]
                else:
                    user.settings = stt.UserSettings()
            usr.update_by_id(users)
        else:
            # Initialize and insert new user
            user = usr.User()
            user.session_id = request.sid
            user.user_ip = request.host
            user.active = True
            user = usr.insert(user)
            # Initialize and insert new user settings
            user_settings = stt.UserSettings()
            user_settings.user_id = user.identity
            user.settings = stt.insert(user_settings)
    except Exception as err:
        print(err)
    join_room(request.sid)
    print('client_connected::{}'.format(request.sid))


# Flask socket disconnect event handler
@SOCKET_IO.on('disconnect', namespace='/server')
def on_disconnect():
    """ Function that handles a socket disconnect event """
    try:
        users = usr.select_by_ip(request.host)
        for user in users:
            user.active = False
            user_settings = stt.select_by_user_id(user.identity)
            if user_settings:
                user.settings = user_settings[0]
            else:
                user.settings = stt.UserSettings()
        usr.update_by_id(users)
    except Exception as err:
        print(err)
    leave_room(request.sid)
    print('client_disconnected::{}'.format(request.sid))


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


if __name__ == '__main__':
    main()
