import datetime
import database.schema as db


class FileSystem():
    id = None
    name = None
    type = None
    path = None
    active = None
    date_created = None
    date_modified = None

    def __init__(self,  *initial_data, **kwards):
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
                                  db.func.max(db.file_systems.c.id, type_=db.Integer).
                                  label('max')
                              ])).scalar()
        return max_id + 1 if max_id else 1


def insert(file_system):
    with db.database_engine.connect() as conn:
        system = dict(file_system)
        system['id'] = new_id()
        system['date_created'] = datetime.datetime.now()
        system['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     file_systems.
                     insert(), system)
        return FileSystem(system)


def insert_collection(file_system_collection):
    with db.database_engine.connect() as conn:
        collection = []
        id_interval = 0
        for entry in file_system_collection:
            system = dict(entry)
            system['id'] = new_id() + id_interval
            system['date_created'] = datetime.datetime.now()
            system['date_modified'] = datetime.datetime.now()
            collection.append(system)
            id_interval += 1
        conn.execute(db.
                     file_systems.
                     insert(), collection)
        return [FileSystem(entry) for entry in collection]


def update_by_id(file_system):
    with db.database_engine.connect() as conn:
        system = dict(file_system)
        system['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     file_systems.
                     update().
                     where(db.file_systems.c.id == system['id']).
                     values(system))
        return FileSystem(system)


def update_by_path(file_system):
    with db.database_engine.connect() as conn:
        system = dict(file_system)
        system['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     file_systems.
                     update().
                     where(db.file_systems.c.id == system['id']).
                     values(system))
        return FileSystem(system)


def update_collection(file_system_collection):
    collection = []
    for file_system in file_system_collection:
        system = dict(file_system)
        system['date_modified'] = datetime.datetime.now()
        conn.execute(db.
                     file_system.
                     update().
                     values(system))
        collection.append(system)
    return [FileSystem(system) for system in collection]


def delete_by_id(id):
    with db.database_engine.connect() as conn:
        conn.execute(db.
                     file_systems.
                     delete().
                     where(db.file_systems.c.id == id))


def delete_by_path(path):
    with db.database_engine.connect() as conn:
        conn.execute(db.
                     file_systems.
                     delete().
                     where(db.file_systems.c.path == path))


def select_by_id(id):
    with db.database_engine.connect() as conn:
        file_system_collection = conn.execute(db.
                                              select([db.file_systems]).
                                              where(db.file_systems.c.id == id))
        return FileSystem(dict(file_system_collection.fetchone()))


def select_by_path(path):
    with db.database_engine.connect() as conn:
        file_system_collection = conn.execute(db.
                                              select([db.file_systems]).
                                              where(db.file_systems.c.path == path))
        return list(map(lambda system: FileSystem(dict(system)), file_system_collection))


def select_active():
    with db.database_engine.connect() as conn:
        file_system_collection = conn.execute(db.
                                              select([db.file_systems]).
                                              where(db.file_systems.c.active == True))
        return list(map(lambda system: FileSystem(dict(system)), file_system_collection))
