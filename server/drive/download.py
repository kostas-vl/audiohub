""" Contains functions for downloading an mp3 using youtube dl """
import sys
import subprocess
import collections
import drive.file_system as file_system
from enviroment import SOCKET_IO, emit


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


@SOCKET_IO.on('download', namespace='/server')
def download(data):
    """ A function that downloads the provided url on the provided path """
    system_name = data['system']
    url = data['url']
    file_format = data['fileFormat']
    system = file_system.select_by_name(system_name)
    if isinstance(system, collections.Sequence) and system:
        path = system[0].path
        download_url(path, url, file_format)
        emit('download finished')
