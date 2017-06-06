""" File containing code that revolves around the playlist data table """
import datetime
from database.schema import DATABASE, select, func, Integer


class Playlist():
    """ A class representing the playlist data table """
    id = None
    name = None
    type = None
    path = None
    active = None
    date_created = None
    date_modified = None

    def __init__(self, *initial_data, **kwards):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

        for key in kwards:
            setattr(self, key, kwards[key])

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'type', self.type
        yield 'path', self.path
        yield 'active', self.active
        yield 'date_created', '' if not self.date_created else self.date_created.isoformat()
        yield 'date_modified', '' if not self.date_modified else self.date_modified.isoformat()


def new_id():
    """ A function that produces a new id for the playlist data table """
    with DATABASE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.max(
                    DATABASE.playlist.c.id, type_=Integer
                ).label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(playlist):
    """ A function that inserts a new entry on the playlist data table """
    with DATABASE.engine.connect() as conn:
        entry = dict(playlist)
        entry['id'] = new_id()
        entry['date_created'] = datetime.datetime.now()
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE.playlist.insert(), entry
        )
        return Playlist(entry)


def insert_collection(playlist_collection):
    """ A function that inserts a collection of entries on the playlist data table """
    with DATABASE.engine.connect() as conn:
        collection = []
        id_interval = 0
        for playlist in playlist_collection:
            entry = dict(playlist)
            entry['id'] = new_id() + id_interval
            entry['date_created'] = datetime.datetime.now()
            entry['date_modified'] = datetime.datetime.now()
            collection.append(entry)
            id_interval += 1
        conn.execute(
            DATABASE.playlist.insert(), collection
        )
        return [Playlist(entry) for entry in collection]


def update_by_id(playlist):
    """ A function that updates an entry on the playlist data table
        that contains tha provided playlist id
    """
    with DATABASE.engine.connect() as conn:
        entry = dict(playlist)
        entry['date_created'] = datetime.datetime.strptime(
            entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
        )
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE.
            playlist.
            update().
            where(DATABASE.playlist.c.id == entry['id']).
            values(entry)
        )
        return Playlist(entry)


def update_by_path(playlist):
    """ A function that updates an entry on the playlist data table
        that contains the provided playlist path
    """
    with DATABASE.engine.connect() as conn:
        entry = dict(playlist)
        entry['date_created'] = datetime.datetime.strptime(
            entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
        )
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE.
            playlist.
            update().
            where(DATABASE.playlist.c.path == entry['path']).
            values(entry)
        )
        return Playlist(entry)


def update_collection(playlist_collection):
    """ A function that updates a collection of entries on the playlist data table """
    collection = []
    with DATABASE.engine.connect() as conn:
        for playlist in playlist_collection:
            entry = dict(playlist)
            entry['date_created'] = datetime.datetime.strptime(
                entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            entry['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE.
                playlist.
                update().
                values(entry)
            )
            collection.append(entry)
        return [Playlist(entry) for entry in collection]


def delete_all():
    """ A function that deletes all entries in the playlist data table """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            playlist.
            delete()
        )


def delete_by_id(playlist_id):
    """ A function that deletes an entry for the playlist data table
        that contains the provided id
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            playlist.
            delete().
            where(DATABASE.playlist.c.id == playlist_id)
        )


def delete_by_path(path):
    """ A function that deletes an entry for the playlist data table
        that contains the provided playlist path
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            playlist.
            delete().
            where(DATABASE.playlist.c.path == path)
        )


def select_by_id(id):
    """ A function that returns all the entries on the playlist data table
        that contain the provided playlist id
    """
    with DATABASE.engine.connect() as conn:
        playlist_collection = conn.execute(
            select([DATABASE.playlist]).
            where(DATABASE.playlist.c.id == id)
        )
        return Playlist(dict(playlist_collection.fetchone()))


def select_by_path(path):
    """ A function that returns all the entries of the playlist data table
        that contain the provided playlist path
    """
    with DATABASE.engine.connect() as conn:
        playlist_collection = conn.execute(
            select([DATABASE.playlist]).
            where(DATABASE.playlist.c.path == path)
        )
        return list(map(lambda entry: Playlist(dict(entry)), playlist_collection))


def select_active_by_path(path):
    """ A function taht returns all the active entries on the playlist data table
        for the provided path
    """
    with DATABASE.engine.connect() as conn:
        playlist_collection = conn.execute(
            select([DATABASE.playlist]).
            where(
                DATABASE.playlist.c.path == path and DATABASE.playlist.c.active == True
            )
        )
        return list(map(lambda entry: Playlist(dict(entry)), playlist_collection))


def select_active():
    """ A function that returns all the active entries on the playlist data table """
    with DATABASE.engine.connect() as conn:
        playlist_collection = conn.execute(
            select([DATABASE.playlist]).
            where(DATABASE.playlist.c.active == True)
        )
        return list(map(lambda entry: Playlist(dict(entry)), playlist_collection))
