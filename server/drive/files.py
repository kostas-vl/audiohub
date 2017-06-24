""" Contains all the file oriented event handlers for the socket io server namespace """
import os
import models.file_system as fs
import drive.network as net
from flask_socketio import emit
from enviroment import SOCKET_IO


def build_dir_tree(path):
    """ A function that returns all the directories and files for the provided path """
    tree = []
    if path:
        entries = os.listdir(path)
        for entry in entries:
            system_type = 'directory' if os.path.isdir(path + entry) else 'file'
            fse = fs.FileSystem(name=entry, type=system_type, path=path + entry)
            tree.append(fse)
    return tree


@SOCKET_IO.on('available systems', namespace='/server')
def on_available_systems(data):
    """ A function that emits to all the connections all the available file systems """
    emit_available_systems()


@SOCKET_IO.on('list dir', namespace='/server')
def on_list_dir(data):
    """ A function that emits all the files and directories for the provided path """
    tree = build_dir_tree(data)
    emit('list dir', [dict(node) for node in tree])


@SOCKET_IO.on('add volume', namespace='/server')
def on_add_volume(data):
    """ A function that adds a volume on the list of available systems and then
        emits its contents
    """
    if os.path.isdir(data['path']):
        file_system = fs.insert(fs.FileSystem(
            name=data['name'],
            type='directory',
            path=data['path'],
            active=True
        ))
        emit('add volume success', dict(file_system))


@SOCKET_IO.on('mount volume', namespace='/server')
def on_mount_volume(data):
    """ A function that mounts a volume on the list of available systems
        and then emits its contents
    """
    details = net.NetworkFileSystem(
        ip=data['ip'],
        volume=data['volume'],
        user=data['user'],
        password=data['password'],
        persistent=True
    )
    mount_path = net.mount(details)
    mount_name = 'Mount: ' + mount_path

    file_system = fs.insert(fs.FileSystem(
        name=mount_name, type='directory', path=mount_path, active=True))
    emit('mount volume success', dict(file_system))


@SOCKET_IO.on('remove volume', namespace='/server')
def on_remove_volume(data):
    """ A function that removes a volume from the list of available systems and then
        emits its contents
    """
    if data:
        fs.delete_by_id(data)
        emit_available_systems()


def emit_available_systems():
    """ A function that emits the list of available systems """
    emit('available systems', [dict(entry) for entry in fs.select_active()])
