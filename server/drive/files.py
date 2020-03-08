"""
Contains all the file oriented event handlers for the socket io server namespace
"""
import os
import models.file_system as fs
import drive.network as net
from flask_socketio import emit
from enviroment import SOCKET_IO


def build_dir_tree(path):
    """
    A function that returns all the directories and files for the provided path
    """
    tree = []
    if path:
        entries = os.listdir(path)
        available_formats = ['.wav', '.mp3', '.mp4']
        for entry in entries:
            fse = fs.FileSystem(
                name=entry,
                path=os.path.join(path, entry)
            )
            if os.path.isdir(fse.path):
                fse.type = 'directory'
                tree.append(fse)
            else:
                _, ext = os.path.splitext(fse.path)
                if ext in available_formats:
                    fse.type = 'file'
                    tree.append(fse)
        return tree


@SOCKET_IO.on('available systems', namespace='/server')
def on_available_systems(_):
    """
    A function that emits to all the connections all the available file systems
    """
    emit_available_systems()


@SOCKET_IO.on('list dir', namespace='/server')
def on_list_dir(data):
    """
    A function that emits all the files and directories for the provided path
    """
    tree = build_dir_tree(data)
    emit('list dir', [dict(node) for node in tree])


@SOCKET_IO.on('add volume', namespace='/server')
def on_add_volume(data):
    """
    A function that adds a volume on the list of available systems and then
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
    else:
        emit('add volume failure')


@SOCKET_IO.on('mount volume', namespace='/server')
def on_mount_volume(data):
    """
    A function that mounts a volume on the list of available systems
    and then emits its contents
    """
    details = net.NetworkFileSystem(
        ip_address=data['ip'],
        directory=data['volume'],
        user=data['user'],
        password=data['password'],
        persistent=True
    )
    mount_path = net.mount(details)
    if mount_path:
        mount_name = '(Network) ' + details.directory
        file_system = fs.insert(
            fs.FileSystem(
                name=mount_name,
                type='directory',
                path=mount_path,
                active=True
            )
        )
        emit('mount volume success', dict(file_system))
    else:
        emit('mount volume failure')


@SOCKET_IO.on('remove volume', namespace='/server')
def on_remove_volume(data):
    """
    A function that removes a volume from the list of available systems and then
    emits its contents
    """
    if data:
        fs.delete_by_id(data)
        emit_available_systems()


def emit_available_systems():
    """
    A function that emits the list of available systems
    """
    emit('available systems', [dict(entry) for entry in fs.select_active()])
