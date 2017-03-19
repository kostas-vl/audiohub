import os
import sys
import samba
import config
import enviroment
from enum import Enum
from file_system_entry import *
from enviroment import *


def build_dir_tree(path):
    entries = os.listdir(path)
    tree = []

    for entry in entries:
        type = 'directory' if os.path.isdir(path + entry) else 'file'
        fse = FileSystemEntry(entry, type, path + entry)
        tree.append(fse)

    return tree


def change_current_system(name):
    selected_file_system = config.systems


@socketio.on('available systems', namespace='/server')
def available_file_systems(data):
    emit('available systems', [dict(entry) for entry in config.systems])


@socketio.on('list dir', namespace='/server')
def list_dir(data):
    tree = build_dir_tree(data)
    emit('list dir', [dict(node) for node in tree])


@socketio.on('mount volume', namespace='/server')
def mount_volume(data):
    details = samba.SambaDetails(
        ip_address=data['ip'], volume=data['volume'], user=data['user'], password=data['password'], persistent=True)

    mount_path = samba.mount(details)
    mount_name = 'Mount: ' + mount_path

    file_system_entry = FileSystemEntry(mount_name, 'directory', mount_path)
    config.systems.append(file_system_entry)
    emit('mount volume success', dict(file_system_entry))


@socketio.on('save volume', namespace='/server')
def save_volume(data):
    config.systems.append(FileSystemEntry(
        data['name'], 'directory', data['path']))
