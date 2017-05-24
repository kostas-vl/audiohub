""" Contains functions for downloading an mp3 using youtube dl """
import os
import subprocess
import collections
import drive.file_system as file_system
from enviroment import SOCKET_IO, emit


def youtube_dl_command(path, url):
    """ A function that returns the command for downloading an mp3 with youtube dl """
    youtube_dl = ''
    if os.name == 'nt':
        youtube_dl = 'youtube-dl.exe'
    elif os.name == 'posix':
        youtube_dl = 'youtube_dl'
    return ''.join([
        youtube_dl,
        '--extract-audio --audio-format mp3 -o ',
        path + "'%(title)s.%(ext)s'" + ' ',
        url
    ])


def download_url(path, url):
    """ A function that executes a shell command to download the provided url
        on the provided path using youtube dl
    """
    try:
        command = youtube_dl_command(path, url)
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as err:
        print(err)


@SOCKET_IO.on('download', namespace='/server')
def download(data):
    """ A function that downloads the provided url on the provided path """
    path = data['path']
    system = file_system.select_by_path(path)
    if isinstance(system, collections.Sequence) and system:
        download_url(path, data['url'])
        emit('download finished')
