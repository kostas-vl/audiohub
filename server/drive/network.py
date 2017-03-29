import sys
import os
import subprocess
from enviroment import *
from subprocess import call

connections = []
files = []


class NetworkFileSystem():
    ip = ''
    volume = ''
    user = ''
    password = ''
    persistent = True

    def __init__(self, ip, volume, user, password='', persistent=False):
        self.ip = ip_address
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
    persistent = 'yes' if details.persistent else 'no'

    command = 'net use \\\\{0}\{1} {2} /user:{3} /persistent:{4}'.format(
        details.ip, details.volume, details.password, details.user, persistent)
    call(command.split())

    connections.append(details)

    mount_path = '\\\\' + details.ip + '\\' + details.volume + '\\'
    return mount_path


def nt_unmount(details):
    path = '\\\\' + details.ip + '\\' + details.volume
    command = 'net use {0} /delete'.format(path)
    call(command.split())


def posix_mount(details):
    pass


def posix_unmount(details):
    pass


def java_mount(details):
    pass


def java_unmount(details):
    pass
