""" Contains functions for mounting and unmounting network file systems """
import os
import subprocess


class NetworkFileSystem():
    """ Class representing a network file system details """
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
    """ A function that mounts a new network file system """
    if os.name == 'nt':
        return nt_mount(details)
    elif os.name == 'posix':
        return posix_mount(details)
    elif os.name == 'java':
        return java_mount(details)
    else:
        return ''


def unmount(details):
    """ A function that unmounts a network file system """
    if os.name == 'nt':
        nt_unmount(details)
    elif os.name == 'posix':
        posix_unmount(details)
    elif os.name == 'java':
        java_unmount(details)
    else:
        pass


def nt_mount(details):
    """ A function that mounts a new network file system on a windows OS """
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

    except subprocess.CalledProcessError as err:
        print(err)
        return None


def nt_unmount(details):
    """ A function that unmounts a network file system on a windows OS """
    try:
        path = '\\\\' + details.ip + '\\' + details.volume
        command = 'net use {0} /delete'.format(path)

        result = subprocess.run(command.split(), shell=True, check=True)
        result.check_returncode()

        return 0

    except subprocess.CalledProcessError:
        return None


def posix_mount(details):
    """ A function that mounts a new network file system on a posix OS """
    pass


def posix_unmount(details):
    """ A function that unmounts a network file system on a posix OS """
    pass


def java_mount(details):
    """ JAVAAAAAAAA """
    pass


def java_unmount(details):
    """ JAVAAAAAAAA """
    pass
