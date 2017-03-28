import datetime
import database.schema as db


class Playlist():
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
        yield 'date_created', self.date_created
        yield 'date_modified', self.date_modified


def insert(playlist):
    with db.database_engine.connect() as conn:
        entry = dict(playlist)
        entry['id'] = db.func.max(db.playlist.c.id)
        entry['date_created'] = datetime.datetime.now()
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     playlist.
                     insert(), entry)
        return Playlist(entry)


def insert_collection(playlist_collection):
    with db.database_engine.connect() as conn:
        collection = []
        for playlist in playlist_collection:
            entry = dict(playlist)
            entry['id'] = db.func.max(db.playlist.c.id)
            entry['date_created'] = datetime.datetime.now()
            entry['date_modified'] = datetime.datetime.now()
            collection.append(entry)
        conn.execute(db.
                     playlist.
                     insert(), collection)
        return [Playlist(entry) for entry in collection]


def update_by_id(playlist):
    with db.database_engine.connect() as conn:
        entry = dict(playlist)
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     playlist.
                     update().
                     where(db.playlist.c.id == entry['id']).
                     values(entry))
        return Playlist(entry)


def update_by_path(playlist):
    with db.database_engine.connect() as conn:
        entry = dict(playlist)
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     playlist.
                     update().
                     where(db.playlist.c.path == entry['path']).
                     values(entry))
        return Playlist(entry)


def update_collection(playlist_collection):
    collection = []
    with db.database_engine.connect() as conn:
        for playlist in playlist_collection:
            entry = dict(playlist)
            entry['date_modified'] = datetime.datetime.now()
            conn.execute(db.
                         playlist.
                         update().
                         values(entry))
            collection.append(entry)
        return [Playlist(entry) for entry in collection]


def select_active():
    with db.database_engine.connect() as conn:
        collection = conn.execute(db.
                                  select([db.playlist]).
                                  where(db.playlist.c.active == True))
        return list(map(lambda entry: Playlist(dict(entry)), collection))
