import subprocess
import drive.file_system as file_system
from enviroment import *


def download_url(path, url):
    try:
        command = [
            'youtube-dl -o',
            path + '"%(title)s.%(ext)s"',
            url
        ]
        command = ['ls']
        command_result = subprocess.run('net use', shell=True, check=True)        
        command_result.check_returncode()
    except CalledProcessError as err:
        print(err)


@socketio.on('download', namespace='/server')
def download(data):
    path = data['path']
    system = file_system.select_by_path(path)
    if len(system) > 0:
        download_url(path, data['url'])
