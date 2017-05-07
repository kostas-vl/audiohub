""" Contains functions for downloading an mp3 using youtube dl """
import subprocess
import collections
import drive.file_system as file_system
from enviroment import SOCKET_IO

def download_url(path, url):
    """ A function that executes a shell command to download the provided url
        on the provided path using youtube dl
    """
    try:
        command = [
            'youtube-dl.exe --extract-audio --audio-format mp3 -o ',
            path + "'%(title)s.%(ext)s'" + ' ',
            url
        ]
        command_result = subprocess.run(
            ''.join(command), shell=True, check=True)
        command_result.check_returncode()
    except subprocess.CalledProcessError as err:
        print(err)


@SOCKET_IO.on('download', namespace='/server')
def download(data):
    """ A function that downloads the provided url on the provided path """
    path = data['path']
    system = file_system.select_by_path(path)
    if isinstance(system, collections.Sequence) and system:
        download_url(path, data['url'])
