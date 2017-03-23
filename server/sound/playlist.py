import datetime
import database.schema as db


class Playlist():
    Id = None
    Name = None
    Type = None
    Path = None
    Active = None
    DateCreated = None
    DateModified = None

    def __init__(self, *initial_data, **kwards):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key.title().replace('_', ''), dictionary[key])

        for key in kwards:
            setattr(self, key.title().replace('_', ''), kwards[key])

    def __iter__(self):
        yield 'id', self.Id
        yield 'name', self.Name
        yield 'type', self.Type
        yield 'path', self.Path
        yield 'active', self.Active
        yield 'date_created', self.DateCreated
        yield 'date_modified', self.DateModified


def insert(playlist):
    with db.database_engine.connect() as conn:
        insert = db.playlist.insert()
        conn.execute(insert, [dict(playlist)])


def insertCollection(playlistCollection):
    with db.database_engine.connect() as conn:
        insert = db.playlist.insert()
        conn.execute(insert, [dict(entry) for entry in playlistCollection])


def selectActive():
    with db.database_engine.connect() as conn:
        collection = conn.execute(db.
                                  select([db.playlist]).
                                  where(db.playlist.c.active == True))
        return map(lambda entry: Playlist(dict(entry)), collection)
