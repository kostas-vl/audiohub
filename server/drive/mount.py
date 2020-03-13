"""
Module that exposes methods for mounting network folders.
"""
import os
import sys
import subprocess


def mount(details):
    """
    A function that mounts a new network file system
    """
    if sys.platform == 'win32':
        return win32_mount(details)
    if sys.platform == 'linux':
        return linux_mount(details)
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
        win_path = '\\\\' + details.ip_address + '\\' + details.directory
        path = '//' + details.ip_address + '/' + details.directory + '/'
        subprocess.check_call(' '.join([
            'net use',
            win_path,
            details.password,
            '/user:' + details.user,
            '/persistent:' + persistent
        ]), shell=True)
        return path
    except subprocess.CalledProcessError as err:
        print(err)
        return None


def win32_unmount(details):
    """
    A function that unmounts a network file system on a windows OS
    """
    try:
        path = '\\\\' + details.ip_address + '\\' + details.directory
        subprocess.check_call(' '.join([
            'net use',
            path,
            '/delete'
        ]), shell=True)
    except subprocess.CalledProcessError as err:
        print(err)


def linux_mount(details):
    """
    A function that mounts a new network file system on a posix OS
    """
    # Create all the directory paths (network and local)
    current_dir = os.path.abspath(os.path.curdir)
    mnt_network_directory = '//' + details.ip_address + '/' + details.directory
    mnt_local_directory = current_dir + '/mnt/' + details.directory
    try:
        # If the local directory doesnt exist, create it
        if not os.path.exists(mnt_local_directory):
            os.makedirs(mnt_local_directory)
        subprocess.check_call(' '.join([
            'mount',
            '-t',
            'cifs',
            mnt_network_directory,
            mnt_local_directory,
            '-o',
            'rw',
            '-o',
            'user="' + details.user + '",' + 'password="' + details.password + '"',
        ]), shell=True)
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
        subprocess.check_call(' '.join([
            'umount',
            '-a',
            '-t',
            'cifs'
        ]), shell=True)
    except subprocess.CalledProcessError as err:
        print(err)
