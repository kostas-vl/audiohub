"""
Contains the user class implementation
"""
import collections
import datetime
from models.base_model import BaseModel
from database import DATABASE_INSTANCE
from sqlalchemy import Integer, select, func


class User(BaseModel):
    """
    Class that contains the information of a user
    """

    def __init__(self, *initial_data, **kwords):
        self.identity = None
        self.user_ip = None
        self.session_id = None
        self.active = False
        self.date_created = None
        self.date_modified = None
        self.settings = None
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'identity', self.identity
        yield 'user_ip', self.user_ip
        yield 'session_id', self.session_id
        yield 'active', self.active
        if self.date_created:
            yield 'date_created', self.date_created.isoformat()
        else:
            yield 'date_created', ''
        if self.date_modified:
            yield 'date_modified', self.date_modified.isoformat()
        else:
            yield 'date_modified', ''
        if self.settings:
            yield 'settings', dict(self.settings)
        else:
            yield 'settings', ''


def new_id():
    """
    A function that produces a new id for the users data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.
                max(DATABASE_INSTANCE.users.c.identity, type_=Integer).
                label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(data):
    """
    A function that inserts new entries on the users data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        if isinstance(data, User) and data:
            # Insert user
            user = dict(data)
            user['identity'] = new_id()
            user['date_created'] = datetime.datetime.now()
            user['date_modified'] = datetime.datetime.now()
            del user['settings']
            conn.execute(
                DATABASE_INSTANCE.users.insert(), user
            )
            return User(user)
        if isinstance(data, collections.Sequence) and data:
            user_collection = []
            id_interval = 0
            for entry in data:
                user = dict(entry)
                user_id = new_id() + id_interval
                user['identity'] = user_id
                user['date_created'] = datetime.datetime.now()
                user['date_modified'] = datetime.datetime.now()
                del user['settings']
                user_collection.append(user)
                id_interval += 1
            conn.execute(
                DATABASE_INSTANCE.users.insert(), user_collection
            )
            return list(map(User, user_collection))
        return None


def update(data):
    """
    A function that updates entries on the users data table
    """
    if isinstance(data, User):
        with DATABASE_INSTANCE.engine.connect() as conn:
            user = dict(data)
            user['date_created'] = datetime.datetime.strptime(
                user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            user['date_modified'] = datetime.datetime.now()
            del user['settings']
            conn.execute(
                DATABASE_INSTANCE.
                users.
                update().
                values(user)
            )
            user['settings'] = data.settings
            return User(user)
    if isinstance(data, collections.Sequence) and data:
        with DATABASE_INSTANCE.engine.connect() as conn:
            user_collection = []
            for entry in data:
                user = dict(entry)
                user['date_created'] = datetime.datetime.strptime(
                    user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                user['date_modified'] = datetime.datetime.now()
                del user['settings']
                conn.execute(
                    DATABASE_INSTANCE.
                    users.
                    update().
                    values(user)
                )
                user['settings'] = entry.settings
                user_collection.append(user)
            return list(map(User, user_collection))
    return None


def update_by_id(data):
    """
    A function that updates an entry on the users data table
    that contains the provided user id
    """
    if isinstance(data, User):
        with DATABASE_INSTANCE.engine.connect() as conn:
            user = dict(data)
            user['date_created'] = datetime.datetime.strptime(
                user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            user['date_modified'] = datetime.datetime.now()
            del user['settings']
            conn.execute(
                DATABASE_INSTANCE.
                users.
                update().
                where(DATABASE_INSTANCE.users.c.identity == data.identity).
                values(user)
            )
            user['settings'] = data.settings
            return User(user)
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            user_collection = []
            for entry in data:
                user = dict(entry)
                user['date_created'] = datetime.datetime.strptime(
                    user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                user['date_modified'] = datetime.datetime.now()
                del user['settings']
                conn.execute(
                    DATABASE_INSTANCE.
                    users.
                    update().
                    where(DATABASE_INSTANCE.users.c.identity == entry.identity).
                    values(user)
                )
                user_collection.append(user)
            return list(map(User, user_collection))
    return None


def delete(data):
    """
    A function that deletes entries from the users data table
    """
    if isinstance(data, User):
        with DATABASE_INSTANCE.engine.connect() as conn:
            conn.execute(
                DATABASE_INSTANCE.
                users.
                delete().
                where(DATABASE_INSTANCE.users.c.identity == data.identity)
            )
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            for entry in data:
                conn.execute(
                    DATABASE_INSTANCE.
                    users.
                    delete().
                    where(DATABASE_INSTANCE.users.c.identity == entry.identity)
                )


def delete_all():
    """
    A function that deletes all entries in the users date table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(DATABASE_INSTANCE.users.delete())


def delete_by_id(file_id):
    """
    A function that removes an entry from the users data table
    that contains the provided id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(
            DATABASE_INSTANCE.
            users.
            delete().
            where(DATABASE_INSTANCE.users.c.identity == file_id)
        )


def select_by_id(user_id):
    """
    A function that returns the entry on the user data table
    with the provided id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.users]).
            where(DATABASE_INSTANCE.users.c.identity == user_id)
        )
        return [User(dict(x)) for x in collection]


def select_by_ip(user_ip):
    """
    A function that returns the entry on the user data table
    with the provided session id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.users]).
            where(DATABASE_INSTANCE.users.c.user_ip == user_ip)
        )
        return [User(dict(x)) for x in collection]


def select_active():
    """
    A function that returns all active users from the users data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.users]).
            where(DATABASE_INSTANCE.users.c.active == True)
        )
        return [User(dict(x)) for x in collection]
