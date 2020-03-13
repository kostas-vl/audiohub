"""
Contains the streams class implementation
"""
import collections
import datetime
import uuid
import sqlalchemy as sql
from models.base_model import BaseModel
from database import DATABASE_INSTANCE


class Stream(BaseModel):
    """
    Class that contains the information of a stream
    """

    def __init__(self, *initial_data, **kwords):
        self.identity = None
        self.title = None
        self.url = None
        self.player_url = None
        self.date_created = None
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'identity', self.identity
        yield 'title', self.title
        yield 'url', self.url
        yield 'player_url', self.player_url
        if self.date_created:
            yield 'date_created', self.date_created.isoformat()
        else:
            yield 'date_created', ''


def insert(data):
    """
    A function that inserts new entries on the stream data table
    """
    if isinstance(data, Stream) and data:
        with DATABASE_INSTANCE.engine.connect() as conn:
            stream = dict(data)
            stream['identity'] = str(uuid.uuid4())
            stream['date_created'] = datetime.datetime.now()
            conn.execute(
                DATABASE_INSTANCE.streams.insert(), stream
            )
            return Stream(stream)
    if isinstance(data, collections.Sequence) and data:
        with DATABASE_INSTANCE.engine.connect() as conn:
            collection = []
            for entry in data:
                stream = dict(entry)
                stream['identity'] = str(uuid.uuid4())
                stream['date_created'] = datetime.datetime.now()
                collection.append(stream)
            conn.execute(
                DATABASE_INSTANCE.streams.insert(), stream
            )
            return [Stream(x) for x in collection]
    return None

def update(data):
    """
    A function that updates entries of the stream data table
    """
    if isinstance(data, Stream):
        with DATABASE_INSTANCE.engine.connect() as conn:
            stream = dict(data)
            stream['date_created'] = datetime.datetime.strptime(
                stream['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            conn.execute(
                DATABASE_INSTANCE.
                streams.
                update().
                where(DATABASE_INSTANCE.streams.c.identity == data.identity).
                values(stream)
            )
            return Stream(stream)
    if isinstance(data, collections.Sequence):
        with DATABASE_INSTANCE.engine.connect() as conn:
            collection = []
            for entry in data:
                stream = dict(entry)
                stream['date_created'] = datetime.datetime.strptime(
                    stream['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                conn.execute(
                    DATABASE_INSTANCE.
                    streams.
                    update().
                    where(DATABASE_INSTANCE.streams.c.identity == entry.identity).
                    values(stream)
                )
                collection.append(stream)
            return [Stream(x) for x in collection]
    return None

def select():
    """
    A function that returns all the entries on the stream data table
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            sql.select([DATABASE_INSTANCE.streams])
        )
        return [Stream(dict(x)) for x in collection]


def select_by_id(identity):
    """
    A function that returns all the entries on the stream data table that contain
    the provided identity
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            sql.
            select([DATABASE_INSTANCE.streams]).
            where(DATABASE_INSTANCE.streams.c.identity == identity)
        )
        return [Stream(dict(x)) for x in collection]


def select_by_url(url):
    """
    A function that returns all the entries on the stream data table that contain
    the provided url
    """
    with DATABASE_INSTANCE.engine.connect() as conn:
        collection = conn.execute(
            sql.
            select([DATABASE_INSTANCE.streams]).
            where(DATABASE_INSTANCE.streams.c.url == url)
        )
        return [Stream(dict(x)) for x in collection]
