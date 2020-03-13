"""
Contains the user settings class implementation and functions for
database interaction.
"""
import collections
import datetime
from models.base_model import BaseModel
from sqlalchemy import Integer, select, func
from database import DATABASE_INSTANCE


class UserSettings(BaseModel):
    """
    Class that contains the information for the settings of a user
    """

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
        if self.date_created:
            yield 'date_created', self.date_created.isoformat()
        else:
            yield 'date_modified', ''
        if self.date_modified:
            yield 'date_modified', self.date_modified.isoformat()
        else:
            yield 'date_modified', ''


def new_id():
    """
    A function that produces a new id for the user settings data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        max_id = conn.execute(
            select([
                func.
                max(DATABASE_INSTANCE.user_settings.c.identity, type_=Integer).
                label('max')
            ])
        ).scalar()
        return max_id + 1 if max_id else 1


def insert(data):
    """
    A function that inserts new entries on the user settings data table
    """
    if isinstance(data, UserSettings):
        with DATABASE_INSTANCE.engine.connect() as conn:
            settings = dict(data)
            settings['identity'] = new_id()
            settings['date_created'] = datetime.datetime.now()
            settings['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE_INSTANCE.user_settings.insert(), dict(settings)
            )
            return UserSettings(settings)
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            collection = []
            id_interval = 0
            for entry in data:
                settings = dict(entry)
                settings['identity'] = new_id() + id_interval
                settings['date_created'] = datetime.datetime.now()
                settings['date_modified'] = datetime.datetime.now()
                collection.append(settings)
                id_interval += 1
            conn.execute(
                DATABASE_INSTANCE.users.insert(), settings_collection
            )
            return [UserSettings(x) for x in collection]
    return None


def update(data):
    """
    A function that updates entries on the user settings data table
    """
    if isinstance(data, UserSettings):
        with DATABASE_INSTANCE.engine.connect() as conn:
            settings = dict(data)
            settings['date_created'] = datetime.datetime.strptime(
                settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            settings['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE_INSTANCE.
                user_settings.
                update().
                values(settings)
            )
            return UserSettings(settings)
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            collection = []
            for entry in data:
                settings = dict(entry)
                settings['date_created'] = datetime.datetime.strptime(
                    settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                settings['date_modified'] = datetime.datetime.now()
                conn.execute(
                    DATABASE_INSTANCE.
                    user_settings.
                    update().
                    values(settings)
                )
                collection.append(settings)
            return [UserSettings(x) for x in collection]
    return None


def update_by_id(data):
    """
    A function that updates an entry on the user settings data table
    that contains the provided id
    """
    if isinstance(data, UserSettings):
        with DATABASE_INSTANCE.engine.connect() as conn:
            settings = dict(data)
            settings['date_created'] = datetime.datetime.strptime(
                settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            settings['date_modified'] = datetime.datetime.now()
            conn.execute(
                DATABASE_INSTANCE.
                user_settings.
                update().
                where(DATABASE_INSTANCE.user_settings.c.identity == data.identity).
                values(settings)
            )
            return UserSettings(settings)
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            collection = []
            for entry in data:
                settings = dict(entry)
                settings['date_creted'] = datetime.datetime.strptime(
                    settings['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                settings['date_modified'] = datetime.datetime.now()
                conn.execute(
                    DATABASE_INSTANCE.
                    user_settings.
                    update().
                    where(DATABASE_INSTANCE.user_settings.c.identity == entry.identity).
                    values(settings)
                )
                collection.append(settings)
            return [UserSettings(x) for x in collection]
    return None


def delete(data):
    """
    A function that deletes entries from the user settings data table
    """
    if isinstance(data, UserSettings):
        with DATABASE_INSTANCE.engine.connect() as conn:
            conn.execute(
                DATABASE_INSTANCE.
                user_settings.
                delete().
                where(DATABASE_INSTANCE.user_settings.c.identity == data.identity)
            )
    elif isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            for entry in data:
                conn.execute(
                    DATABASE_INSTANCE.
                    user_settings.
                    delete().
                    where(DATABASE_INSTANCE.user_settings.c.identity == entry.identity)
                )
    else:
        pass


def delete_all():
    """
    A function that deletes all entries in the users date table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(DATABASE_INSTANCE.user_settings.delete())


def delete_by_id(identity):
    """
    A function that removes an entry from the user settings data table
    that contains the provided id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        conn.execute(
            DATABASE_INSTANCE.
            user_settings.
            delete().
            where(DATABASE_INSTANCE.user_settings.c.identity == identity)
        )


def select_by_id(settings_id):
    """
    A function that returns the entry on the user settings data table with
    the provided id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.user_settings]).
            where(DATABASE_INSTANCE.user_settings.c.identity == settings_id)
        )
        return list(map(lambda x: UserSettings(dict(x)), collection))


def select_by_user_id(user_id):
    """
    A function that returns the entry on the user settings data table
    with the provided user id
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            select([DATABASE_INSTANCE.user_settings]).
            where(DATABASE_INSTANCE.user_settings.c.user_id == user_id)
        )
        return list(map(lambda x: UserSettings(dict(x)), collection))
