""" Contains the user class implementation """
import collections
import datetime
from base.model import Model
from database.schema import DATABASE, Integer, select, func


class UserSettings(Model):
    """ Class that contains the information for the settings of a user """

    def __init__(self, *initial_data, **kwords):
        self.identity = None
        self.user_id = None
        self.sound_direction = 'server'
        self.dark_theme = True
        self.sidenav_mode = 'side'
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'identity', self.identity
        yield 'user_id', self.user_id
        yield 'sound_direction', self.sound_direction
        yield 'dark_theme', self.dark_theme
        yield 'sidenav_mode', self.sidenav_mode


class User(Model):
    """ Class that contains the information of a user """

    def __init__(self, *initial_data, **kwords):
        self.identity = None
        self.user_ip = None
        self.session_id = None
        self.active = False
        self.date_created = None
        self.settings = None
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'identity', self.identity
        yield 'user_ip', self.user_ip
        yield 'session_id', self.session_id
        yield 'active', self.active
        yield 'date_created', '' if not self.date_created else self.date_created.isoformat()
        yield 'settings', None if not self.settings else dict(self.settings)


def new_user_id():
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


def new_settings_id():
    """ A function that produces a new id for the user settings data table """
    with DATABASE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.
                max(DATABASE.user_settings.c.identity, type_=Integer).
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
            user['identity'] = new_user_id()
            user['date_created'] = datetime.datetime.now()
            del user['settings']
            conn.execute(
                DATABASE.users.insert(), user
            )
            # Insert settings
            settings = UserSettings()
            settings.identity = new_settings_id()
            settings.user_id = user['identity']
            conn.execute(
                DATABASE.user_settings.insert(), dict(settings)
            )
            user['settings'] = settings
            return User(user)
        # Insert a collection
        elif isinstance(data, collections.Sequence) and data:
            # Construct the collections for the insert
            user_collection = []
            user_settings_collection = []
            id_interval = 0
            for entry in data:
                # Populate a user dictionary and append it
                user = dict(entry)
                user_id = new_user_id() + id_interval
                user['identity'] = user_id
                user['date_created'] = datetime.datetime.now()
                del user['settings']
                user_collection.append(user)
                # Populate a user settings dictionary and append it
                settings = UserSettings()
                settings.identity = new_settings_id() + id_interval
                settings.user_id = user_id
                user_settings_collection.append(dict(settings))
                id_interval += 1
            # Execute the insert statements
            conn.execute(
                DATABASE.users.insert(), user_collection
            )
            conn.execute(
                DATABASE.user_settings.insert(), user_settings_collection
            )
            # Construct a return collection of users
            result = []
            for i, item in enumerate(user_collection):
                user = User(item)
                user.settings = UserSettings(user_settings_collection[i])
                result.append(user)
            return result
        # Insert nothing
        else:
            return None


def update(data):
    """ A function that updates entries on the users data table """
    with DATABASE.engine.connect() as conn:
        # Update a single entry
        if isinstance(data, User) and data:
            user = dict(data)
            settings = dict(data.settings)
            if isinstance(data.date_created, str):
                user['date_created'] = datetime.datetime.strptime(
                    data.date_created, '%Y-%m-%dT%H:%M:%S.%f'
                )
            del user['settings']
            conn.execute(
                DATABASE.
                users.
                update().
                values(user)
            )
            conn.execute(
                DATABASE.
                user_settings.
                update().
                values(settings)
            )
            user['settings'] = UserSettings(settings)
            return User(user)
        # Update a collection
        elif isinstance(data, collections.Sequence) and data:
            user_collection = []
            user_settings_collection = []
            for entry in data:
                # Configure the user and settings dictionaries
                user = dict(entry)
                settings = dict(entry.settings)
                if isinstance(entry.date_created, str):
                    user['date_created'] = datetime.datetime.strptime(
                        entry.date_created, '%Y-%m-%dT%H:%M:%S.%f'
                    )
                del user['settings']
                # Append the new entries
                user_collection.append(user)
                user_settings_collection.append(settings)
                # Execute the update statements
                conn.execute(
                    DATABASE.
                    users.
                    update().
                    values(user)
                )
                conn.execute(
                    DATABASE.
                    user_settings.
                    update().
                    values(settings)
                )
            result = []
            for i, item in enumerate(user_collection):
                user = User(item)
                settings = UserSettings(user_settings_collection[i])
                user.settings = settings
                result.append(user)
            return result
        # Update nothing
        else:
            return None


def update_by_id(data):
    """ A function that updates an entry on the users data table
        that contains the provided user id
    """
    with DATABASE.engine.connect() as conn:
        user = dict(data)
        settings = data.settings
        if isinstance(data.date_created, str):
            user['date_created'] = datetime.datetime.strptime(
                data.date_created, '%Y-%m-%dT%H:%M:%S.%f'
            )
        del user['settings']
        conn.execute(
            DATABASE.
            users.
            update().
            where(DATABASE.users.c.identity == data.identity).
            values(user)
        )
        conn.execute(
            DATABASE.
            user_settings.
            update().
            where(DATABASE.user_settings.c.user_id == data.identity).
            values(settings)
        )
        user['settings'] = UserSettings(settings)
        return User(user)


def delete(data):
    """ A function that deletes entries from the users data table """
    with DATABASE.engine.connect() as conn:
        if isinstance(data, tuple):
            user, settings = data
            # Deleting the user settings
            conn.execute(
                DATABASE.
                user_settings.
                delete().
                where(DATABASE.user_settings.c.identity == settings.identity)
            )
            # Deleting the user
            conn.execute(
                DATABASE.
                users.
                delete().
                where(DATABASE.users.c.identity == user.identity)
            )
        if isinstance(data, collections.Sequence):
            for entry in data:
                user, settings = entry
                # Deleting the user settings
                conn.execute(
                    DATABASE.
                    user_settings.
                    delete().
                    where(DATABASE.user_settings.c.identity == settings.identity)
                )
                # Deleting the user
                conn.execute(
                    DATABASE.
                    users.
                    delete().
                    where(DATABASE.users.c.identity == user.identity)
                )


def delete_all():
    """ A function that deletes all entries in the users date table """
    with DATABASE.engine.connect() as conn:
        conn.execute(DATABASE.user_settings.delete())
        conn.execute(DATABASE.users.delete())


def delete_by_id(id):
    """ A function that removes an entry from the users data table
        that contains the provided id
    """
    with DATABASE.engine.connect() as conn:
        # Deleting the user settings
        conn.execute(
            DATABASE.
            user_settings.
            delete().
            where(DATABASE.users.c.user_id == id)
        )
        # Deleting the user
        conn.execute(
            DATABASE.
            users.
            delete().
            where(DATABASE.users.c.identity == id)
        )


def select_by_id(id):
    """ A function that returns the entry on the user data table with the provided id """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.users]).
            where(DATABASE.users.c.identity == id)
        )
        users = list(map(lambda x: User(dict(x)), collection))
        for user in users:
            settings_collection = conn.execute(
                select([DATABASE.user_settings]).
                where(DATABASE.user_settings.c.user_id == id)
            )
            settings = list(
                map(lambda x: UserSettings(dict(x)), settings_collection))
            if settings:
                user.settings = UserSettings(settings[0])
            else:
                user.settings = UserSettings()
        return users


def select_by_ip(user_ip):
    """ A function that returns the entry on the user data table with the provided session id """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.users]).
            where(DATABASE.users.c.user_ip == user_ip)
        )
        users = list(map(lambda x: User(dict(x)), collection))
        for user in users:
            settings_collection = conn.execute(
                select([DATABASE.user_settings]).
                where(DATABASE.user_settings.c.user_id == user.identity)
            )
            settings = list(
                map(lambda x: UserSettings(dict(x)), settings_collection))
            if settings:
                user.settings = UserSettings(settings[0])
            else:
                user.settings = UserSettings()
        return users


def select_active():
    """ A function that returns all active users from the users data table """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.users]).
            where(DATABASE.users.c.active == True)
        )
        users = list(map(lambda entry: User(dict(entry)), collection))
        for user in users:
            settings_collection = conn.execute(
                select([DATABASE.users]).
                where(DATABASE.users.c.user_id == user.identity)
            )
            settings = list(
                map(lambda x: UserSettings(dict(x)), settings_collection))
            if settings:
                user.settings = UserSettings(settings[0])
            else:
                user.settings = UserSettings()
        return users
