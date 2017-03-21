import json
import sqlite3
from file_system_entry import *

database = 'audiohub.db'

queries_file_path = './queries.json'

queries = None

systems = []

playlist = []


def load_queries():
    global queries
    queries = {}
    with open(queries_file_path, 'r') as queries_file:
        content = json.loads(queries_file.read())
        for key, value in content.items():
            queries[key] = "".join(value)


def create_systems_table():
    with sqlite3.connect(database) as conn:
        conn.cursor().execute(queries['CREATE_SYSTEMS'])


def create_playlist_table():
    with sqlite3.connect(database) as conn:
        conn.cursor().execute(queries['CREATE_PLAYLIST'])


def drop_systems_table():
    with sqlite3.connect(database) as conn:
        conn.cursor().execute(queries['DROP_SYSTEMS'])


def drop_playlist_table():
    with sqlite3.connect(database) as conn:
        conn.cursor().execute(queries['DROP_PLAYLIST'])


def insert_system(file_entry):
    with sqlite3.connect(database) as conn:
        query = queries['INSERT_SYSTEM'].format(
            file_entry.Name, file_entry.Type, file_entry.Path, '', 0)


def insert_playlist(file_entry):
    with sqlite3.connect(database) as conn:
        query = queries['INSERT_PLAYLIST'].format(
            file_entry.Name, file_entry.Type, file_entry.Path, '', 0)


def update_system_by_id(file_entry):
    with sqlite3.connect(database) as conn:
        conn.cursor().execute(queries['UPDATE_SYSTEM_BY_ID'].format(id))


def load():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        print(cursor.execute(queries['LOAD_SYSTEM_QUERIES']))

    # with open('./config.json') as file:
    #     file_content = file.read()
    #     decoded_content = json.loads(file_content)

    #     for entry in decoded_content['systems']:
    #         systems.append(FileSystemEntry(
    #             entry['name'], entry['type'], entry['path']))

    #     for entry in decoded_content['playlist']:
    #         playlist.append(FileSystemEntry(
    #             entry['name'], entry['type'], entry['path']))


def update():
    encoded_content = {
        'systems': [dict(entry) for entry in systems],
        'playlist': [dict(entry) for entry in playlist]
    }
    with open('./config.json') as file:
        file.write(json.dumps(encoded_content, sort_keys=False, indent=4))
