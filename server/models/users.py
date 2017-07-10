""" Contains the user class implementation """
import collections
import datetime
from base.model import Model
from database.schema import DATABASE
from sqlalchemy import Integer, select, func


class User(Model):
    """ Class that contains the information of a user """

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
        yield 'date_created', '' if not self.date_created else self.date_created.isoformat()
        yield 'date_modified', '' if not self.date_modified else self.date_modified.isoformat()
        yield 'settings', None if not self.settings else dict(self.settings)


def new_id():
    """ A function that produces a new id for the users data table """
    with DATABASE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.
                max(DATABASE.users.c.identity, type_=Integer).
                label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(data):
    """ A function that inserts new entries on the users data table """
    with DATABASE.engine.connect() as conn:
        # Insert a single entry
        if isinstance(data, User) and data:
            # Insert user
            user = dict(data)
            user['identity'] = new_id()
            user['date_created'] = datetime.datetime.now()
            user['date_modified'] = datetime.datetime.now()
            del user['settings']
            conn.execute(
                DATABASE.users.insert(), user
            )
            return User(user)
        # Insert a collection
        elif isinstance(data, collections.Sequence) and data:
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
                DATABASE.users.insert(), user_collection
            )
            return list(map(User, user_collection))
        # Insert nothing
        else:
            return None


def update(data):
    """ A function that updates entries on the users data table """
    # Update a single entry
    if isinstance(data, User):
        with DATABASE.engine.connect() as conn:
            user = dict(data)
            user['date_created'] = datetime.datetime.strptime(
                user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            user['date_modified'] = datetime.datetime.now()
            del user['settings']
            conn.execute(
                DATABASE.
                users.
                update().
                values(user)
            )
            user['settings'] = data.settings
            return User(user)
    # Update a collection
    elif isinstance(data, collections.Sequence) and data:
        with DATABASE.engine.connect() as conn:
            user_collection = []
            for entry in data:
                user = dict(entry)
                user['date_created'] = datetime.datetime.strptime(
                    user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                user['date_modified'] = datetime.datetime.now()
                del user['settings']
                conn.execute(
                    DATABASE.
                    users.
                    update().
                    values(user)
                )
                user['settings'] = entry.settings
                user_collection.append(user)
            return list(map(User, user_collection))
    # Update nothing
    else:
        return None


def update_by_id(data):
    """ A function that updates an entry on the users data table
        that contains the provided user id
    """
    if isinstance(data, User):
        with DATABASE.engine.connect() as conn:
            user = dict(data)
            user['date_created'] = datetime.datetime.strptime(
                user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            user['date_modified'] = datetime.datetime.now()
            del user['settings']
            conn.execute(
                DATABASE.
                users.
                update().
                where(DATABASE.users.c.identity == data.identity).
                values(user)
            )
            user['settings'] = data.settings
            return User(user)
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            user_collection = []
            for entry in data:
                user = dict(entry)
                user['date_created'] = datetime.datetime.strptime(
                    user['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                user['date_modified'] = datetime.datetime.now()
                del user['settings']
                conn.execute(
                    DATABASE.
                    users.
                    update().
                    where(DATABASE.users.c.identity == entry.identity).
                    values(user)
                )
                user_collection.append(user)
            return list(map(User, user_collection))
    else:
        return None


def delete(data):
    """ A function that deletes entries from the users data table """
    if isinstance(data, User):
        with DATABASE.engine.connect() as conn:
            conn.execute(
                DATABASE.
                users.
                delete().
                where(DATABASE.users.c.identity == data.identity)
            )
    if isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            for entry in data:
                conn.execute(
                    DATABASE.
                    users.
                    delete().
                    where(DATABASE.users.c.identity == entry.identity)
                )


def delete_all():
    """ A function that deletes all entries in the users date table """
    with DATABASE.engine.connect() as conn:
        conn.execute(DATABASE.users.delete())


def delete_by_id(file_id):
    """ A function that removes an entry from the users data table
        that contains the provided id
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            users.
            delete().
            where(DATABASE.users.c.identity == file_id)
        )


def select_by_id(user_id):
    """ A function that returns the entry on the user data table with the provided id """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.users]).
            where(DATABASE.users.c.identity == user_id)
        )
        return list(map(lambda x: User(dict(x)), collection))


def select_by_ip(user_ip):
    """ A function that returns the entry on the user data table with the provided session id """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.users]).
            where(DATABASE.users.c.user_ip == user_ip)
        )
        return list(map(lambda x: User(dict(x)), collection))


def select_active():
    """ A function that returns all active users from the users data table """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.users]).
            where(DATABASE.users.c.active == True)
        )
        return list(map(lambda x: User(dict(x)), collection))
