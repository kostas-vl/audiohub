"""
Module that exposes method for downloading audio files from various websites.
"""
import sys
import subprocess
from configuration import APP_SETTINGS_INSTANCE


def youtube_dl_command(path, url, file_format):
    """
    A function that returns the command for downloading an mp3 with youtube dl
    """
    youtube_dl = ''
    filepath = ''
    if sys.platform == 'win32':
        youtube_dl = APP_SETTINGS_INSTANCE.youtube.win32_path
        filepath = path + "%(title)s.%(ext)s"
    elif sys.platform == 'linux':
        youtube_dl = APP_SETTINGS_INSTANCE.youtube.linux_path
        filepath = "'" + path + "%(title)s.%(ext)s" + "'"
    return ' '.join([
        youtube_dl,
        '--extract-audio',
        '--audio-format',
        file_format,
        '-o',
        filepath,
        url
    ])


def download_url(path, url, file_format):
    """
    A function that executes a shell command to download the provided url
    on the provided path using youtube dl
    """
    try:
        command = youtube_dl_command(path, url, file_format)
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as err:
        print(err)
