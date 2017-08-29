"""
File containing code that revolves around the file systems data table
"""
import collections
import datetime
from sqlalchemy import Integer, select, func
from base.model import Model
from database.schema import DATABASE


class FileSystem(Model):
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
        yield 'date_created', '' if not self.date_created else self.date_created.isoformat()
        yield 'date_modified', '' if not self.date_modified else self.date_modified.isoformat()


def new_id():
    """
    A function that produces a new id for the file systems data table
    """
    with DATABASE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.
                max(DATABASE.file_systems.c.identity, type_=Integer).
                label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(data):
    """
    A function that inserts a new entry on the file systems data table
    """

    # Insert a single entry
    if isinstance(data, FileSystem):
        with DATABASE.engine.connect() as conn:
            system = dict(data)
            system['identity'] = new_id()
            system['date_created'] = datetime.datetime.now()
            system['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE.file_systems.insert(), system
            )
            return FileSystem(system)
    # Insert a collection
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
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
                DATABASE.file_systems.insert(), collection
            )
            return [FileSystem(entry) for entry in collection]
    # Insert nothing
    else:
        return None


def update(data):
    """
    A function that updates a collection of entries on the file systems data table
    """
    # Update single entry
    if isinstance(data, FileSystem):
        with DATABASE.engine.connect() as conn:
            system = dict(data)
            if isinstance(system['date_created'], str):
                system['date_created'] = datetime.datetime.strptime(
                    data.date_created, '%Y-%m-%dT%H:%M:%S.%f'
                )
            system['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE.
                file_systems.
                update().
                values(system)
            )
            return FileSystem(system)
    # Update a collection
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            collection = []
            for entry in data:
                system = dict(entry)
                if isinstance(system['date_created'], str):
                    system['date_created'] = datetime.datetime.strptime(
                        entry.date_created, '%Y-%m-%dT%H:%M:%S.%f'
                    )
                system['date_modified'] = datetime.datetime.now()
                conn.execute(
                    DATABASE.
                    file_systems.
                    update().
                    values(collection)
                )
                collection.append(system)
            return [FileSystem(system) for system in collection]
    # Update nothing
    else:
        return None


def update_by_id(file_system):
    """
    A function that updates an entry on the file systems data table
    that contains the provided file system id
    """
    with DATABASE.engine.connect() as conn:
        system = dict(file_system)
        system['date_created'] = datetime.datetime.strptime(
            system['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
        )
        system['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE.
            file_systems.
            update().
            where(DATABASE.file_systems.c.identity == file_system.identity).
            values(system)
        )
        return FileSystem(system)


def update_by_path(file_system):
    """
    A function that updates an entry on the file systems data table
    that contains the provided file system path
    """
    with DATABASE.engine.connect() as conn:
        system = dict(file_system)
        if isinstance(system['date_created', str]):
            system['date_created'] = datetime.datetime.strptime(
                system['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
        system['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE.
            file_systems.
            update().
            where(DATABASE.file_systems.c.path == file_system.path).
            values(system)
        )
        return FileSystem(system)


def delete_all():
    """
    A function that deletes all entries in the file systems data table
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(DATABASE.file_systems.delete())


def delete_by_id(identity):
    """
    A function that deletes an entry for the file system data table
    that contains the provided id
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            file_systems.
            delete().
            where(DATABASE.file_systems.c.identity == identity)
        )


def delete_by_path(path):
    """
    A function that deletes an entry for the file system data table
    that contains the provided system path
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            file_systems.
            delete().
            where(DATABASE.file_systems.c.path == path)
        )


def select_by_id(identity):
    """
    A function that returns all the entries on the file systems data table
    that contain the provided system id
    """
    with DATABASE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE.file_systems]).
            where(DATABASE.file_systems.c.identity == identity)
        )
        return FileSystem(dict(file_system_collection.fetchone()))


def select_by_path(path):
    """
    A function that returns all the entries of the file systems data table
    that contain the provided system path
    """
    with DATABASE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE.file_systems]).
            where(DATABASE.file_systems.c.path == path)
        )
        return list(map(lambda x: FileSystem(dict(x)), file_system_collection))


def select_by_name(name):
    """
    A function that returns all the entires of the file systems data table
    that contain the provided system name
    """
    with DATABASE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE.file_systems]).
            where(DATABASE.file_systems.c.name == name)
        )
        return list(map(lambda x: FileSystem(dict(x)), file_system_collection))


def select_active():
    """
    A function that returns all the active entries on the file systems data table
    """
    with DATABASE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE.file_systems]).
            where(DATABASE.file_systems.c.active == True)
        )
        return list(map(lambda x: FileSystem(dict(x)), file_system_collection))
