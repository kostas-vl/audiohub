""" File containing code that revolves around the file systems data table """
import datetime
from database.schema import DATABASE, select, func, Integer


class FileSystem():
    """ A class representing the file systems data table """
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
    """ A function that produces a new id for the file systems data table """
    with DATABASE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.
                max(DATABASE.file_systems.c.id, type_=Integer).
                label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(file_system):
    """ A function that inserts a new entry on the file systems data table """
    with DATABASE.engine.connect() as conn:
        system = dict(file_system)
        system['id'] = new_id()
        system['date_created'] = datetime.datetime.now()
        system['date_modified'] = datetime.datetime.now()
        conn.execute(
            DATABASE.file_systems.insert(), system
        )
        return FileSystem(system)


def insert_collection(file_system_collection):
    """ A function that inserts a collection of entries on the file systems data table """
    with DATABASE.engine.connect() as conn:
        collection = []
        id_interval = 0
        for entry in file_system_collection:
            system = dict(entry)
            system['id'] = new_id() + id_interval
            system['date_created'] = datetime.datetime.now()
            system['date_modified'] = datetime.datetime.now()
            collection.append(system)
            id_interval += 1
        conn.execute(
            DATABASE.file_systems.insert(), collection
        )
        return [FileSystem(entry) for entry in collection]


def update_by_id(file_system):
    """ A function that updates an entry on the file systems data table
        that contains tha provided file system id
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
            where(DATABASE.file_systems.c.id == system['id']).
            values(system)
        )
        return FileSystem(system)


def update_by_path(file_system):
    """ A function that updates an entry on the file systems data table
        that contains the provided file system path
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
            where(DATABASE.file_systems.c.id == system['id']).
            values(system)
        )
        return FileSystem(system)


def update_collection(file_system_collection):
    """ A function that updates a collection of entries on the file systems data table """
    collection = []
    with DATABASE.engine.connect() as conn:
        for file_system in file_system_collection:
            system = dict(file_system)
            system['date_created'] = datetime.datetime.strptime(
                system['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            system['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE.
                file_systems.
                update().
                values(system)
            )
            collection.append(system)
    return [FileSystem(system) for system in collection]


def delete_by_id(system_id):
    """ A function that deletes an entry for the file system data table
        that contains the provided id
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            file_systems.
            delete().
            where(DATABASE.file_systems.c.id == system_id)
        )


def delete_by_path(path):
    """ A function that deletes an entry for the file system data table
        that contains the provided system path
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            file_systems.
            delete().
            where(DATABASE.file_systems.c.path == path)
        )


def select_by_id(system_id):
    """ A function that returns all the entries on the file systems data table
        that contain the provided system id
    """
    with DATABASE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE.file_systems]).
            where(DATABASE.file_systems.c.id == system_id)
        )
        return FileSystem(dict(file_system_collection.fetchone()))


def select_by_path(path):
    """ A function that returns all the entries of the file systems data table
        that contain the provided system path
    """
    with DATABASE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE.file_systems]).
            where(DATABASE.file_systems.c.path == path)
        )
        return list(map(lambda system: FileSystem(dict(system)), file_system_collection))


def select_active():
    """ A function that returns all the active entries on the file systems data table """
    with DATABASE.engine.connect() as conn:
        file_system_collection = conn.execute(
            select([DATABASE.file_systems]).
            where(DATABASE.file_systems.c.active == True)
        )
        return list(map(lambda system: FileSystem(dict(system)), file_system_collection))
