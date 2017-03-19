import json
from file_system_entry import *

systems = []

selected_system = FileSystemEntry('', '', '')

playlist = []


def load():
    file = open('./config.json', 'r')
    file_content = file.read()
    decoded_content = json.loads(file_content)

    for entry in decoded_content['systems']:
        systems.append(FileSystemEntry(
            entry['name'], entry['type'], entry['path']))

    for entry in decoded_content['playlist']:
        playlist.append(FileSystemEntry(
            entry['name'], entry['type'], entry['path']))

    selected_system_dict = decoded_content['selectedSystem']
    selected_system = FileSystemEntry(selected_system_dict['name'], selected_system_dict[
                                      'type'], selected_system_dict['path'])


def update():
    encoded_content = {
        'systems': [dict(entry) for entry in systems],
        'selectedSystem': dict(selected_system),
        'playlist': [dict(entry) for entry in playlist]
    }
    file = open('./config.json', 'w')
    file.write(json.dumps(encoded_content, sort_keys=False, indent=4))
