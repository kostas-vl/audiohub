#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains functions for downloading an mp3 using youtube dl
"""
import collections
import drive
import models.file_system as fs
from flask import request
from enviroment import APP, SOCKET_IO


def download_async(sid, path, url, file_format):
    """
    Downloads a track with youtube dl and then send an emit when
    the call is finished.
    """
    drive.download_url(path, url, file_format)
    with APP.test_request_context('/'):
        SOCKET_IO.emit('download finished', namespace='/server', room=sid)


@SOCKET_IO.on('download', namespace='/server')
def on_download(data):
    """
    A function that downloads the provided url on the provided path
    """
    system_name = data['system']
    system = fs.select_by_name(system_name)
    if isinstance(system, collections.Sequence) and system:
        SOCKET_IO.start_background_task(
            download_async,
            request.sid,
            system[0].path,
            data['url'],
            data['fileFormat']
        )
