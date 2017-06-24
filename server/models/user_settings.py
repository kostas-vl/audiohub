""" Contains the user settings class implementation and functions for database interaction """
import collections
import datetime
from database.schema import DATABASE, select, func, Integer
from base.model import Model


class UserSettings(Model):
    """ Class that contains the information for the settings of a user """

    def __init__(self, *initial_data, **kwords):
        self.identity = None
        self.user_id = None
        self.sound_direction = 'server'
        self.dark_theme = True
        self.sidenav_mode = 'side'
        self.date_created = None
        self.date_modified = None
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'identity', self.identity
        yield 'user_id', self.user_id
        yield 'sound_direction', self.sound_direction
        yield 'dark_theme', self.dark_theme
        yield 'sidenav_mode', self.sidenav_mode
        yield 'date_created', '' if not self.date_created else self.date_created.isoformat()
        yield 'date_modified', '' if not self.date_created else self.date_modified.isoformat()


def new_id():
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
    """ A function that inserts new entries on the user settings data table """
    # Insert a signle entry
    if isinstance(data, UserSettings):
        with DATABASE.engine.connect() as conn:
            # Insert settings
            settings = dict(data)
            settings['identity'] = new_id()
            settings['date_created'] = datetime.datetime.now()
            settings['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE.user_settings.insert(), dict(settings)
            )
            return UserSettings(settings)
    # Insert a collection
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            settings_collection = []
            id_interval = 0
            for entry in data:
                settings = dict(entry)
                settings['identity'] = new_id() + id_interval
                settings['date_created'] = datetime.datetime.now()
                settings['date_modified'] = datetime.datetime.now()
                settings_collection.append(settings)
                id_interval += 1
            conn.execute(
                DATABASE.users.insert(), settings_collection
            )
            return list(map(UserSettings, settings_collection))
    # Insert nothing
    else:
        return None


def update(data):
    """ A function that updates entries on the user settings data table """
    # Update a single entry
    if isinstance(data, UserSettings):
        with DATABASE.engine.connect() as conn:
            settings = dict(data)
            settings['date_created'] = datetime.datetime.strptime(
                settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            settings['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE.
                user_settings.
                update().
                values(settings)
            )
            return UserSettings(settings)
    # Update a collection
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            settings_collection = []
            for entry in data:
                settings = dict(entry)
                settings['date_created'] = datetime.datetime.strptime(
                    settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                settings['date_modified'] = datetime.datetime.now()
                conn.execute(
                    DATABASE.
                    user_settings.
                    update().
                    values(settings)
                )
                settings_collection.append(settings)
            return list(map(UserSettings, settings_collection))
    # Update nothing
    else:
        return None


def update_by_id(data):
    """ A function that updates an entry on the user settings data table
        that contains the provided id
    """
    # Update single entry
    if isinstance(data, UserSettings):
        with DATABASE.engine.connect() as conn:
            settings = dict(data)
            settings['date_creted'] = datetime.datetime.strptime(
                settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            settings['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE.
                user_settings.
                update().
                where(DATABASE.user_settings.c.identity == data.identity).
                values(data)
            )
            return UserSettings(settings)
    # Update a collection
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            settings_collection = []
            for entry in data:
                settings = dict(entry)
                settings['date_creted'] = datetime.datetime.strptime(
                    settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                settings['date_modified'] = datetime.datetime.now()
                conn.execute(
                    DATABASE.
                    user_settings.
                    update().
                    where(DATABASE.user_settings.c.identity == entry.identity).
                    values(settings)
                )
                settings_collection.append(settings)
            return list(map(UserSettings, settings_collection))
    # Update nothing
    else:
        return None


def delete(data):
    """ A function that deletes entries from the user settings data table """
    if isinstance(data, UserSettings):
        with DATABASE.engine.connect() as conn:
            conn.execute(
                DATABASE.
                user_settings.
                delete().
                where(DATABASE.user_settings.c.identity == data.identity)
            )
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            for entry in data:
                conn.execute(
                    DATABASE.
                    user_settings.
                    delete().
                    where(DATABASE.user_settings.c.identity == entry.identity)
                )
    else:
        pass


def delete_all():
    """ A function that deletes all entries in the users date table """
    with DATABASE.engine.connect() as conn:
        conn.execute(DATABASE.user_settings.delete())


def delete_by_id(id):
    """ A function that removes an entry from the user settings data table
        that contains the provided id
    """
    with DATABASE.engine.connect() as conn:
        conn.execute(
            DATABASE.
            user_settings.
            delete().
            where(DATABASE.user_settings.c.identity == id)
        )


def select_by_id(settings_id):
    """ A function that returns the entry on the user settings data table with the provided id """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.user_settings]).
            where(DATABASE.user_settings.c.identity == settings_id)
        )
        return list(map(lambda x: UserSettings(dict(x)), collection))


def select_by_user_id(user_id):
    """ A function that returns the entry on the user settings data table
        with the provided user id
    """
    with DATABASE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE.user_settings]).
            where(DATABASE.user_settings.c.user_id == user_id)
        )
        return list(map(lambda x: UserSettings(dict(x)), collection))
