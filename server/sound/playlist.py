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
        yield 'date_created', '' if not self.date_created else self.date_created.isoformat()
        yield 'date_modified', '' if not self.date_modified else self.date_modified.isoformat()


def new_id():
    with db.database_engine.connect() as conn:
        max_id = conn.execute(db.
                              select([
                                  db.
                                  func.
                                  max(db.playlist.c.id,
                                      type_=db.Integer).label('max')
                              ])).scalar()
        return max_id + 1 if max_id else 1


def insert(playlist):
    with db.database_engine.connect() as conn:
        entry = dict(playlist)
        entry['id'] = new_id()
        entry['date_created'] = datetime.datetime.now()
        entry['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     playlist.
                     insert(), entry)
        return Playlist(entry)


def insert_collection(playlist_collection):
    with db.database_engine.connect() as conn:
        collection = []
        id_interval = 0
        for playlist in playlist_collection:
            entry = dict(playlist)
            entry['id'] = new_id() + id_interval
            entry['date_created'] = datetime.datetime.now()
            entry['date_modified'] = datetime.datetime.now()
            collection.append(entry)
            id_interval += 1
        conn.execute(db.
                     playlist.
                     insert(), collection)
        return [Playlist(entry) for entry in collection]


def update_by_id(playlist):
    with db.database_engine.connect() as conn:
        entry = dict(playlist)
        entry['date_created'] = datetime.datetime.strptime(
            entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f')
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
        entry['date_created'] = datetime.datetime.strptime(
            entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f')
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
            entry['date_created'] = datetime.datetime.strptime(
                entry['date_created'], '%Y-%m-%dT%H:%M:%S.%f')
            entry['date_modified'] = datetime.datetime.now()
            conn.execute(db.
                         playlist.
                         update().
                         values(entry))
            collection.append(entry)
        return [Playlist(entry) for entry in collection]


def delete_by_id(id):
    with db.database_engine.connect() as conn:
        conn.execute(db.
                     playlist.
                     delete().
                     where(db.playlist.c.id == id))


def delete_by_path(path):
    with db.database_engine.connect() as conn:
        conn.execute(db.
                     playlist.
                     delete().
                     where(db.playlist.c.path == path))


def select_by_id(id):
    with db.database_engine.connect() as conn:
        playlist_collection = conn.execute(db.
                                           select([db.playlist]).
                                           where(db.playlist.c.id == id))
        return Playlist(dict(playlist_collection.fetchone()))


def select_by_path(path):
    with db.database_engine.connect() as conn:
        playlist_collection = conn.execute(db.
                                           select([db.playlist]).
                                           where(db.playlist.c.path == path))
        return list(map(lambda entry: Playlist(dict(entry)), playlist_collection))


def select_active_by_path(path):
    with db.database_engine.connect() as conn:
        playlist_collection = conn.execute(db.
                                           select([db.playlist]).
                                           where(db.playlist.c.path == path and db.playlist.c.active == True))
        return list(map(lambda entry: Playlist(dict(entry)), playlist_collection))


def select_active():
    with db.database_engine.connect() as conn:
        playlist_collection = conn.execute(db.
                                           select([db.playlist]).
                                           where(db.playlist.c.active == True))
        return list(map(lambda entry: Playlist(dict(entry)), playlist_collection))
