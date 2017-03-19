import sys
import os
import subprocess
from enviroment import *
from subprocess import call

connections = []
files = []


class SambaDetails():
    Ip_Address = ''
    Volume = ''
    User = ''
    Password = ''
    Persistent = True

    def __init__(self, ip_address, volume, user, password='', persistent=False):
        self.Ip_Address = ip_address
        self.Volume = volume
        self.User = user
        self.Password = password
        self.Persistent = persistent


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
    persistent = 'yes' if details.Persistent else 'no'

    command = 'net use \\\\{0}\{1} {2} /user:{3} /persistent:{4}'.format(
        details.Ip_Address, details.Volume, details.Password, details.User, persistent)
    call(command.split())

    connections.append(details)

    mount_path = '\\\\' + details.Ip_Address + '\\' + details.Volume + '\\'
    return mount_path


def nt_unmount(details):
    path = '\\\\' + details.Ip_Address + '\\' + details.Volume
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
