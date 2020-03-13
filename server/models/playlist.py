"""
File containing code that revolves around the playlist data table
"""
import datetime
from models.base_model import BaseModel
from sqlalchemy import Integer, select, func
from database import DATABASE_INSTANCE


class Playlist(BaseModel):
    """
    A class representing the playlist data table
    """

    def __init__(self, *initial_data, **kwords):
        self.identity = None
        self.name = None
        self.type = None
        self.path = None
        self.active = None
        self.date_created = None
        self.date_modified = None
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'identity', self.identity
        yield 'name', self.name
        yield 'type', self.type
        yield 'path', self.path
        yield 'active', self.active
        if self.date_created:
            yield 'date_created', self.date_created.isoformat()
        else:
            yield 'date_created', ''
        if self.date_modified:
            yield 'date_modified', self.date_modified.isoformat()
        else:
            yield 'date_modified', ''


def new_id():
    """
    A function that produces a new id for the playlist data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.max(
                    DATABASE_INSTANCE.playlist.c.identity, type_=Integer
                ).label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(playlist):
    """
    A function that inserts a new entry on the playlist data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        entry = dict(playlist)
        entry['identity'] = new_id()
        entry['date_created'] = datetime.datetime.now()
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE_INSTANCE.playlist.insert(), entry
        )
        return Playlist(entry)


def insert_collection(playlist_collection):
    """
    A function that inserts a collection of entries on the playlist data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = []
        id_interval = 0
        for playlist in playlist_collection:
            entry = dict(playlist)
            entry['identity'] = new_id() + id_interval
            entry['date_created'] = datetime.datetime.now()
            entry['date_modified'] = datetime.datetime.now()
            collection.append(entry)
            id_interval += 1
        conn.execute(
            DATABASE_INSTANCE.playlist.insert(), collection
        )
        return [Playlist(entry) for entry in collection]


def update_by_id(playlist):
    """
    A function that updates an entry on the playlist data table
    that contains tha provided playlist id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        entry = dict(playlist)
        entry['date_created'] = datetime.datetime.strptime(
            entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
        )
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE_INSTANCE.
            playlist.
            update().
            where(DATABASE_INSTANCE.playlist.c.identity == entry['identity']).
            values(entry)
        )
        return Playlist(entry)


def update_by_path(playlist):
    """
    A function that updates an entry on the playlist data table
    that contains the provided playlist path
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        entry = dict(playlist)
        entry['date_created'] = datetime.datetime.strptime(
            entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
        )
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE_INSTANCE.
            playlist.
            update().
            where(DATABASE_INSTANCE.playlist.c.path == entry['path']).
            values(entry)
        )
        return Playlist(entry)


def update_collection(playlist_collection):
    """
    A function that updates a collection of entries on the playlist data table
    """
    collection = []
    with DATABASE_INSTANCE.engine.connect() as conn:
        for playlist in playlist_collection:
            entry = dict(playlist)
            entry['date_created'] = datetime.datetime.strptime(
                entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            entry['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE_INSTANCE.
                playlist.
                update().
                values(entry)
            )
            collection.append(entry)
        return [Playlist(entry) for entry in collection]


def delete_all():
    """
    A function that deletes all entries in the playlist data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(
            DATABASE_INSTANCE.
            playlist.
            delete()
        )


def delete_by_id(identity):
    """
    A function that deletes an entry for the playlist data table
    that contains the provided id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(
            DATABASE_INSTANCE.
            playlist.
            delete().
            where(DATABASE_INSTANCE.playlist.c.identity == identity)
        )


def delete_by_path(path):
    """
    A function that deletes an entry for the playlist data table
    that contains the provided playlist path
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(
            DATABASE_INSTANCE.
            playlist.
            delete().
            where(DATABASE_INSTANCE.playlist.c.path == path)
        )


def select_by_id(identity):
    """
    A function that returns all the entries on the playlist data table
    that contain the provided playlist id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        playlist_collection = conn.execute(
            select([DATABASE_INSTANCE.playlist]).
            where(DATABASE_INSTANCE.playlist.c.identity == identity)
        )
        return Playlist(dict(playlist_collection.fetchone()))


def select_by_path(path):
    """
    A function that returns all the entries of the playlist data table
    that contain the provided playlist path
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.playlist]).
            where(DATABASE_INSTANCE.playlist.c.path == path)
        )
        return [Playlist(dict(x)) for x in collection]


def select_active_by_path(path):
    """
    A function taht returns all the active entries on the playlist data table
    for the provided path
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.playlist]).
            where(
                DATABASE_INSTANCE.playlist.c.path == path
                and DATABASE_INSTANCE.playlist.c.active == True
            )
        )
        return [Playlist(dict(x)) for x in collection]


def select_active():
    """
    A function that returns all the active entries on the playlist data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.playlist]).
            where(DATABASE_INSTANCE.playlist.c.active == True)
        )
        return [Playlist(dict(x)) for x in collection]
