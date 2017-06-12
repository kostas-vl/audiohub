""" Contains functions for downloading an mp3 using youtube dl """
import sys
import subprocess
import collections
import drive.file_system as file_system
from flask import request, session
from enviroment import APP, SOCKET_IO, CLIENTS, emit


def youtube_dl_command(path, url, file_format):
    """ A function that returns the command for downloading an mp3 with youtube dl """
    youtube_dl = ''
    if sys.platform == 'win32':
        youtube_dl = 'youtube-dl.exe'
    elif sys.platform == 'linux':
        youtube_dl = 'youtube-dl'
    return ' '.join([
        youtube_dl,
        '--extract-audio',
        '--audio-format',
        file_format,
        '-o',
        path + "%(title)s.%(ext)s",
        url
    ])


def download_url(path, url, file_format):
    """ A function that executes a shell command to download the provided url
        on the provided path using youtube dl
    """
    try:
        command = youtube_dl_command(path, url, file_format)
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as err:
        print(err)


def download_async(sid, path, url, file_format):
    """ Downloads a track with youtube dl and then send an emit when the call is finished """
    download_url(path, url, file_format)
    with APP.test_request_context('/'):
        SOCKET_IO.emit('download finished', namespace='/server', room=sid)


@SOCKET_IO.on('download', namespace='/server')
def on_download(data):
    """ A function that downloads the provided url on the provided path """
    system_name = data['system']
    system = file_system.select_by_name(system_name)
    if isinstance(system, collections.Sequence) and system:
        SOCKET_IO.start_background_task(
            download_async,
            request.sid,
            system[0].path,
            data['url'],
            data['fileFormat']
        )
