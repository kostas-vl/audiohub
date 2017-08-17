""" Contains the streams class implementation """
import collections
import datetime
import uuid
import sqlalchemy as sql
from base.model import Model
from database.schema import DATABASE


class Stream(Model):
    """ Class that contains the information of a stream """

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
        yield 'date_created', '' if not self.date_created else self.date_created.isoformat()


def insert(data):
    """ A function that inserts new entries on the stream data table """
    # Insert a single entry
    if isinstance(data, Stream) and data:
        with DATABASE.engine.connect() as conn:
            # Insert the stream
            stream = dict(data)
            stream['identity'] = str(uuid.uuid4())
            stream['date_created'] = datetime.datetime.now()
            conn.execute(
                DATABASE.streams.insert(), stream
            )
            return Stream(stream)
    # Insert a collection
    elif isinstance(data, collections.Sequence) and data:
        with DATABASE.engine.connect() as conn:
            stream_collection = []
            for entry in data:
                stream = dict(entry)
                stream['identity'] = str(uuid.uuid4())
                stream['date_created'] = datetime.datetime.now()
                stream_collection.append(stream)
            conn.execute(
                DATABASE.streams.insert(), stream
            )
            return list(map(Stream, stream_collection))
    # Insert nothing
    else:
        return None


def update(data):
    """ A function that updates entries of the stream data table """
    # Update a single entry
    if isinstance(data, Stream):
        with DATABASE.engine.connect() as conn:
            stream = dict(data)
            stream['date_created'] = datetime.datetime.strptime(
                stream['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
            )
            conn.execute(
                DATABASE.
                streams.
                update().
                where(DATABASE.streams.c.identity == data.identity).
                values(stream)
            )
            return Stream(stream)
    # Update a collection
    elif isinstance(data, collections.Sequence):
        with DATABASE.engine.connect() as conn:
            stream_collection = []
            for entry in data:
                stream = dict(entry)
                stream['date_created'] = datetime.datetime.strptime(
                    stream['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
                )
                conn.execute(
                    DATABASE.
                    streams.
                    update().
                    where(DATABASE.streams.c.identity == entry.identity).
                    values(stream)
                )
                stream_collection.append(stream)
            return list(map(Stream, stream_collection))
    # Update nothing
    else:
        return None


def select():
    """ A function that returns all the entries on the stream data table """
    with DATABASE.engine.connect() as conn:
        streams = conn.execute(
            sql.select([DATABASE.streams])
        )
        return list(map(lambda x: Stream(dict(x)), streams))


def select_by_id(identity):
    """ A function that returns  all the entries on the stream data table that contain
        the provided identity
    """
    with DATABASE.engine.connect() as conn:
        streams = conn.execute(
            sql.
            select([DATABASE.streams]).
            where(DATABASE.streams.c.identity == identity)
        )
        return list(map(lambda x: Stream(dict(x)), streams))


def select_by_url(url):
    """ A function that returns all the entries on the stream data table that contain
        the provided url
    """
    with DATABASE.engine.connect() as conn:
        streams = conn.execute(
            sql.
            select([DATABASE.streams]).
            where(DATABASE.streams.c.url == url)
        )
        return list(map(lambda x: Stream(dict(x)), streams))