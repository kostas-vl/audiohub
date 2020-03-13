#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains all endpoints for the user's settings.
"""
import models.users as usr
import models.user_settings as stt
from flask import request
from flask_socketio import emit
from enviroment import SOCKET_IO


@SOCKET_IO.on('user settings', namespace='/server')
def on_user_settings(_):
    """
    A function that emits the settings of a user
    """
    users = usr.select_by_ip(request.host)
    if users:
        user = users[0]
        user_settings_collection = stt.select_by_id(user.identity)
        if user_settings_collection:
            settings = user_settings_collection[0]
            emit('user settings', dict(settings))


@SOCKET_IO.on('user settings changed', namespace='/server')
def on_user_settings_changed(data):
    """
    A function that updates the settings of a user based on the provded model
    """
    try:
        if data:
            sent_settings = stt.UserSettings(data)
            users = usr.select_by_ip(request.host)
            if users:
                user_settings_collection = stt.select_by_user_id(
                    users[0].identity
                )
                if user_settings_collection:
                    user_settings = user_settings_collection[0]
                    user_settings.sound_direction = sent_settings.sound_direction
                    user_settings.dark_theme = sent_settings.dark_theme
                    user_settings.sidenav_mode = sent_settings.sidenav_mode
                    stt.update_by_id(user_settings)
    except Exception as err:
        print(err)
