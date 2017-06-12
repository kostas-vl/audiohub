""" Contains functions for mounting and unmounting network file systems """
import sys
import subprocess


class NetworkFileSystem():
    """ Class representing a network file system details """
    ip_address = ''
    directory = ''
    target_directory = ''
    user = ''
    password = ''
    persistent = True

    def __init__(self, *initial_data, **kwords):
        for dictionary in initial_data:
            for key, value in dictionary:
                setattr(self, key, value)

        for key in kwords:
            setattr(self, key, kwords[key])

    def __iter__(self):
        yield 'ip', self.ip_address
        yield 'directory', self.directory
        yield 'target_directory', self.target_directory
        yield 'user', self.user
        yield 'password', self.password
        yield 'persistent', self.persistent


def mount(details):
    """ A function that mounts a new network file system """
    if sys.platform == 'win32':
        return win32_mount(details)
    elif sys.platform == 'linux':
        return linux_mount(details)
    else:
        return ''


def unmount(details):
    """ A function that unmounts a network file system """
    if sys.platform == 'win32':
        win32_unmount(details)
    elif sys.platform == 'linux':
        linux_unmount(details)
    else:
        pass


def win32_mount(details):
    """ A function that mounts a new network file system on a windows OS """
    try:
        persistent = 'yes' if details.persistent else 'no'
        path = '\\\\' + details.ip_address + '\\' + details.volume
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
    """ A function that unmounts a network file system on a windows OS """
    try:
        path = '\\\\' + details.ip_address + '\\' + details.volume
        command = ['net use', path, '/delete']
        subprocess.check_call(' '.join(command), shell=True)
        return 0
    except subprocess.CalledProcessError as err:
        print(err)
        return None


def linux_mount(details):
    """ A function that mounts a new network file system on a posix OS """
    try:
        path = '//' + details.ip_address + '/' + details.volume
        command = [
            'mount',
            '-t',
            'cifs',
            '-o',
            'username=' + details.user,
            'password=' + details.password,
            path,
            details.target_directory
        ]
        subprocess.check_call(' '.join(command), shell=True)
        return details.target_directory + '/'
    except subprocess.CalledProcessError as err:
        print(err)
        return None


def linux_unmount(details):
    """ A function that unmounts a network file system on a posix OS """
    try:
        command = [
            'mount',
            details.target_directory
        ]
        subprocess.check_call(' '.join(command), shell=True)
        return 0
    except subprocess.CalledProcessError as err:
        print(err)
        return None
