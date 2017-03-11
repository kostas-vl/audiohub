import sys
import os
import subprocess
from enviroment import *

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
        nt_mount(details)
    elif os.name == 'posix':
        java_mount(details)
    elif os.name == 'java':
        java_mount(details)
    else:
        pass


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
    # print('net use \\\\{0}\{1} {2} /user:{3} /persistent:{4}'.format(
    #     details.Ip_Address, details.Volume, details.Password, details.User, persistent))
    # os.system('net use \\\\{0}\{1} {2} /user:{3} /persistent:{4}'.format(
    #     details.Ip_Address, details.Volume, details.Password, details.User, persistent))
    command = 'net use \\\\{0}\{1} {2} /user:{3} /persistent:{4}'.format(
        details.Ip_Address, details.Volume, details.Password, details.User, persistent)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    print(output)
    print(error)

    connections.append(details)


def nt_unmount(details):
    os.system(
        'net use \\\\{0}\IPC$ /delete'.format(details.Ip_Address))


def posix_mount(details):
    pass


def posix_unmount(details):
    pass


def java_mount(details):
    pass


def java_unmount(details):
    pass
