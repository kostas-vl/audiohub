"""
File containing code that revolves around the file systems data table
"""
import collections
import datetime
from models.base_model import BaseModel
from sqlalchemy import Integer, select, func
from database import DATABASE_INSTANCE


class FileSystem(BaseModel):
    """
    A class representing the file systems data table
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
    A function that produces a new id for the file systems data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.
                max(DATABASE_INSTANCE.file_systems.c.identity, type_=Integer).
                label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(data):
    """
    A function that inserts a new entry on the file systems data table
    """
    if isinstance(data, FileSystem):
        with DATABASE_INSTANCE.engine.connect() as conn:
            system = dict(data)
            system['identity'] = new_id()
            system['date_created'] = datetime.datetime.now()
            system['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE_INSTANCE.file_systems.insert(), system
            )
            return FileSystem(system)
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            collection = []
            id_interval = 0
            for entry in data:
                system = dict(entry)
                system['identity'] = new_id() + id_interval
                system['date_created'] = datetime.datetime.now()
                system['date_modified'] = datetime.datetime.now()
                collection.append(system)
                id_interval += 1
            conn.execute(
                DATABASE_INSTANCE.file_systems.insert(), collection
            )
            return [FileSystem(entry) for entry in collection]
    return None

def update(data):
    """
    A function that updates a collection of entries on the file systems
    data table
    """
    if isinstance(data, FileSystem):
        with DATABASE_INSTANCE.engine.connect() as conn:
            system = dict(data)
            if isinstance(system['date_created'], str):
                system['date_created'] = datetime.datetime.strptime(
                    data.date_created, '%Y-%m-%dT%H:%M:%S.%f'
                )
            system['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE_INSTANCE.
                file_systems.
                update().
                values(system)
            )
            return FileSystem(system)
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            collection = []
            for entry in data:
                system = dict(entry)
                if isinstance(system['date_created'], str):
                    system['date_created'] = datetime.datetime.strptime(
                        entry.date_created, '%Y-%m-%dT%H:%M:%S.%f'
                    )
                system['date_modified'] = datetime.datetime.now()
                conn.execute(
                    DATABASE_INSTANCE.
                    file_systems.
                    update().
                    values(collection)
                )
                collection.append(system)
            return [FileSystem(system) for system in collection]
    return None


def update_by_id(file_system):
    """
    A function that updates an entry on the file systems data table
    that contains the provided file system id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        system = dict(file_system)
        system['date_created'] = datetime.datetime.strptime(
            system['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
        )
        system['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE_INSTANCE.
            file_systems.
            update().
            where(DATABASE_INSTANCE.file_systems.c.identity == file_system.identity).
            values(system)
        )
        return FileSystem(system)


def update_by_path(file_system):
    """
    A function that updates an entry on the file systems data table
    that contains the provided file system path
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        system = dict(file_system)
        if isinstance(system['date_created', str]):
            system['date_created'] = datetime.datetime.strptime(
                system['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
        system['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE_INSTANCE.
            file_systems.
            update().
            where(DATABASE_INSTANCE.file_systems.c.path == file_system.path).
            values(system)
        )
        return FileSystem(system)


def delete_all():
    """
    A function that deletes all entries in the file systems data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(DATABASE_INSTANCE.file_systems.delete())


def delete_by_id(identity):
    """
    A function that deletes an entry for the file system data table
    that contains the provided id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(
            DATABASE_INSTANCE.
            file_systems.
            delete().
            where(DATABASE_INSTANCE.file_systems.c.identity == identity)
        )


def delete_by_path(path):
    """
    A function that deletes an entry for the file system data table
    that contains the provided system path
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(
            DATABASE_INSTANCE.
            file_systems.
            delete().
            where(DATABASE_INSTANCE.file_systems.c.path == path)
        )


def select_by_id(identity):
    """
    A function that returns all the entries on the file systems data table
    that contain the provided system id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE_INSTANCE.file_systems]).
            where(DATABASE_INSTANCE.file_systems.c.identity == identity)
        )
        return FileSystem(dict(file_system_collection.fetchone()))


def select_by_path(path):
    """
    A function that returns all the entries of the file systems data table
    that contain the provided system path
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.file_systems]).
            where(DATABASE_INSTANCE.file_systems.c.path == path)
        )
        return [FileSystem(dict(x)) for x in collection]


def select_by_name(name):
    """
    A function that returns all the entires of the file systems data table
    that contain the provided system name
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.file_systems]).
            where(DATABASE_INSTANCE.file_systems.c.name == name)
        )
        return [FileSystem(dict(x)) for x in collection]


def select_active():
    """
    A function that returns all the active entries on the file systems
    data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.file_systems]).
            where(DATABASE_INSTANCE.file_systems.c.active == True)
        )
        return [FileSystem(dict(x)) for x in collection]
