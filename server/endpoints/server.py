#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module defines all core endpoints of the application.
"""
import os
import models.users as usr
import models.user_settings as stt
from enviroment import APP, SOCKET_IO
from flask import request, send_from_directory
from flask_socketio import join_room, leave_room


@APP.route('/')
def on_index():
    """
    End point for the '/' path
    """
    return send_from_directory('static', 'index.html')


@APP.route('/<path:path>')
def on_static_file(path):
    """
    Serve any static file
    """
    resource = os.path.join('static', path)
    if os.path.isfile(resource):
        return send_from_directory('static', path)
    return send_from_directory('static', 'index.html')


@SOCKET_IO.on('connect', namespace='/server')
def on_connect():
    """
    Function that handles a new connection socket
    """
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


@SOCKET_IO.on('disconnect', namespace='/server')
def on_disconnect():
    """
    Function that handles a socket disconnect event
    """
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
