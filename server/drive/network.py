import sys
import os
import subprocess
from enviroment import *


class NetworkFileSystem():
    ip = ''
    volume = ''
    user = ''
    password = ''
    persistent = True

    def __init__(self, ip, volume, user, password='', persistent=False):
        self.ip = ip
        self.volume = volume
        self.user = user
        self.password = password
        self.persistent = persistent


def mount(details):
    if os.name == 'nt':
        return nt_mount(details)
    elif os.name == 'posix':
        return posix_mount(details)
    elif os.name == 'java':
        return java_mount(details)
    else:
        return ''


def unmount(details):
    if os.name == 'nt':
        nt_unmount(details)
    elif os.name == 'posix':
        posix_unmount(details)
    elif os.name == 'java':
        java_unmount(details)
    else:
        pass


def nt_mount(details):
    try:
        persistent = 'yes' if details.persistent else 'no'

        command = [
            'net use',
            '\\\\' + details.ip + '\\' + details.volume,
            details.password,
            '/user:' + details.user,
            '/persistent:' + persistent
        ]

        result = subprocess.run(command, shell=True, check=True)
        result.check_returncode()

        return '\\\\' + details.ip + '\\' + details.volume + '\\'

    except subprocess.CalledProcessError:
        return None


def nt_unmount(details):
    try:
        path = '\\\\' + details.ip + '\\' + details.volume
        command = 'net use {0} /delete'.format(path)
        
        result = subprocess.run(command.split(), shell=True, check=True)
        result.check_returncode()

        return 0

    except subprocess.CalledProcessError:
        return None


def posix_mount(details):
    pass


def posix_unmount(details):
    pass


def java_mount(details):
    pass


def java_unmount(details):
    pass
