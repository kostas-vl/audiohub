import os
import sys
import drive.samba
import enviroment
import drive.samba as samba
import drive.file_system as fs
from enum import Enum
from enviroment import *


def build_dir_tree(path):
    entries = os.listdir(path)
    tree = []

    for entry in entries:
        type = 'directory' if os.path.isdir(path + entry) else 'file'
        fse = fs.FileSystem(name=entry, type=type, path=path + entry)
        tree.append(fse)

    return tree


@socketio.on('available systems', namespace='/server')
def available_file_systems(data):
    emit('available systems', [dict(entry) for entry in fs.select_active()])


@socketio.on('list dir', namespace='/server')
def list_dir(data):
    tree = build_dir_tree(data)
    emit('list dir', [dict(node) for node in tree])


@socketio.on('add volume', namespace='/server')
def add_volume(data):
    if os.path.isdir(data['path']):
        file_system = fs.insert(fs.FileSystem(
            name=data['name'], type='directory', path=data['path'], active=True))
        emit('add volume success', dict(file_system))


@socketio.on('mount volume', namespace='/server')
def mount_volume(data):
    details = samba.SambaDetails(
        ip_address=data['ip'], volume=data['volume'], user=data['user'], password=data['password'], persistent=True)

    mount_path = samba.mount(details)
    mount_name = 'Mount: ' + mount_path

    file_system = fs.insert(fs.FileSystem(
        name=mount_name, type='directory', path=mount_path, active=True))
    emit('mount volume success', dict(file_system))


@socketio.on('save volume', namespace='/server')
def save_volume(data):
    data['type'] = 'directory'
    systems.append(fs.FileSystem(data))
