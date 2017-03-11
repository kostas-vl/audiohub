import os
import sys
import samba
import config
from enum import Enum
from enviroment import *


class DirectoryAction(Enum):
    Descend = 0
    Ascend = 1
    Add = 2
    Remove = 3
    Create = 4


class FileSystemEntry():
    Name = ''
    Type = ''
    Path = ''
    Entries = []

    def __init__(self, name, type, path):
        self.Name = name
        self.Type = type
        self.Path = path

    def __iter__(self):
        yield 'name', self.Name
        yield 'type', self.Type
        yield 'path', self.Path
        # yield 'entries', self.Entries


file_systems = [
    FileSystemEntry('Local File System', 'directory',
                    config.LOCAL_FILE_SYSTEM['CURRENT_DIR'])
]

selected_file_system = file_systems[0]


def build_dir_tree(path):
    entries = os.listdir(path)
    tree = []

    for entry in entries:
        type = 'directory' if os.path.isdir(path + entry) else 'file'
        fse = FileSystemEntry(entry, type, path + entry)
        tree.append(fse)

    return tree


def change_current_system(name):
    selected_file_system = file_systems


@socketio.on('available systems', namespace='/server')
def available_file_systems(data):
    # tree = build_dir_tree(config.LOCAL_FILE_SYSTEM['CURRENT_DIR'])
    emit('available systems', [dict(entry) for entry in file_systems])


@socketio.on('list dir', namespace='/server')
def list_dir(data):
    tree = build_dir_tree(data)
    emit('list dir', [dict(node) for node in tree])


@socketio.on('mount volume', namespace='/server')
def mount_volume(data):
    details = samba.SambaDetails(
        ip_address=data['ip'], volume=data['volume'], user=data['user'], password=data['password'], persistent=True)
    samba.mount(details)

    ip_address_str = str(details.Ip_Address)
    mount_path = '/' + ip_address_str + '/' + details.Volume
    mount_name = 'Mount: ' + mount_path

    file_system_entry = FileSystemEntry(mount_name, 'directory', mount_path)
    save_volume(file_system_entry)
    emit('mount volume success', dict(file_system_entry))


@socketio.on('save volume', namespace='/server')
def save_volume(data):
    if os.path.exists(data.name) and os.path.isdir(data.path):
        file_system.append(FileSystemEntry(data.name, 'directory', data.path))
