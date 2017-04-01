import sys
import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData, create_engine, select, delete, bindparam, func

# Engine and Metadata
connection_string = None
database_engine = None
metadata = None

# Tables
file_systems = None
playlist = None


def init(database_settings):
    global connection_string, database_engine, metadata

    connection_string = database_settings['connectionString']
    echo = database_settings['echo']

    if connection_string:
        database_engine = create_engine(connection_string, echo=echo)
        metadata = MetaData()
        file_systems_init()
        playlist_init()
        metadata.create_all(database_engine)
    else:
        raise NameError('Database Connection String not found!')


def file_systems_init():
    global file_systems
    if database_engine and metadata:
        file_systems = Table('file_systems', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('name', String, nullable=False),
                             Column('type', String, nullable=False),
                             Column('path', String, nullable=False),
                             Column('active', Boolean, nullable=False),
                             Column('date_created', DateTime, nullable=False),
                             Column('date_modified', DateTime)
                             )


def playlist_init():
    global playlist
    if database_engine and metadata:
        playlist = Table('playlist', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, nullable=False),
                         Column('type', String, nullable=False),
                         Column('path', String, nullable=False),
                         Column('active', Boolean, nullable=False),
                         Column('date_created', DateTime, nullable=False),
                         Column('date_modified', DateTime)
                         )
