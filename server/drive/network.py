"""
Contains functions for mounting and unmounting network file systems
"""
import os
import sys
import subprocess
from base.model import Model


class NetworkFileSystem(Model):
    """
    Class representing a network file system details
    """

    def __init__(self, *initial_data, **kwords):
        self.ip_address = ''
        self.directory = ''
        self.user = ''
        self.password = ''
        self.persistent = True
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'ip', self.ip_address
        yield 'directory', self.directory
        yield 'user', self.user
        yield 'password', self.password
        yield 'persistent', self.persistent


def mount(details):
    """
    A function that mounts a new network file system
    """
    if sys.platform == 'win32':
        return win32_mount(details)
    elif sys.platform == 'linux':
        return linux_mount(details)
    else:
        return ''


def unmount(details):
    """
    A function that unmounts a network file system
    """
    if sys.platform == 'win32':
        win32_unmount(details)
    elif sys.platform == 'linux':
        linux_unmount(details)
    else:
        pass


def win32_mount(details):
    """
    A function that mounts a new network file system on a windows OS
    """
    try:
        persistent = 'yes' if details.persistent else 'no'
        path = '\\\\' + details.ip_address + '\\' + details.directory
        command = [
            'net use',
            path,
            details.password,
            '/user:' + details.user,
            '/persistent:' + persistent
        ]
        subprocess.check_call(' '.join(command), shell=True)
        return path + '\\'
    except subprocess.CalledProcessError as err:
        print(err)
        return None


def win32_unmount(details):
    """
    A function that unmounts a network file system on a windows OS
    """
    try:
        path = '\\\\' + details.ip_address + '\\' + details.directory
        command = ['net use', path, '/delete']
        subprocess.check_call(' '.join(command), shell=True)
        return 0
    except subprocess.CalledProcessError as err:
        print(err)
        return None


def linux_mount(details):
    """
    A function that mounts a new network file system on a posix OS
    """
    current_dir = os.path.abspath(os.path.curdir)
    mnt_network_directory = '//' + details.ip_address + '/' + details.directory
    mnt_local_directory = current_dir + '/mnt/' + details.directory
    try:
        if not os.path.exists(mnt_local_directory):
            os.makedirs(mnt_local_directory)
        subprocess.check_call([
            'sudo',
            'mount',
            '-t',
            'cifs',
            mnt_network_directory,
            mnt_local_directory,
            '-o',
            'rw',
            '-o',
            'user="' + details.user + '",' + 'password="' + details.password + '"',
        ], shell=True)
        return mnt_local_directory + '/'
    except subprocess.CalledProcessError as err:
        print(err)
        if os.path.exists(mnt_local_directory):
            os.rmdir(mnt_local_directory)
        return None


def linux_unmount(_):
    """
    A function that unmounts a network file system on a posix OS
    """
    try:
        command = [
            'umount',
            '-a',
            '-t',
            'cifs'
        ]
        subprocess.check_call(' '.join(command), shell=True)
        return 0
    except subprocess.CalledProcessError as err:
        print(err)
        return None
