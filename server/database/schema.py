""" Contains functions that initialize the database schema """
import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData, create_engine, select, delete, bindparam, func


class Database():
    """ Class representing the database and the database schema """
    connection_string = None
    engine = None
    metadata = None
    file_systems = None
    playlist = None

    def init(self, database_settings):
        """ A function that initializes  """
        connection_string = database_settings['connectionString']
        echo = database_settings['echo']

        if connection_string:
            self.engine = create_engine(connection_string, echo=echo)
            self.metadata = MetaData()
            self.file_systems = self.file_systems_init()
            self.playlist = self.playlist_init()
            self.metadata.create_all(self.engine)
        else:
            raise NameError('Database Connection String not found!')

    def file_systems_init(self):
        """ A method that initialized the file_systems table """
        if self.engine and self.metadata:
            systems = Table(
                'file_systems',
                self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String, nullable=False),
                Column('type', String, nullable=False),
                Column('path', String, nullable=False),
                Column('active', Boolean, nullable=False),
                Column(
                    'date_created',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                ),
                Column('date_modified', DateTime)
            )
            return systems

    def playlist_init(self):
        """ A method that intializes the playlist table """
        if self.engine and self.metadata:
            playlist = Table(
                'playlist',
                self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String, nullable=False),
                Column('type', String, nullable=False),
                Column('path', String, nullable=False),
                Column('active', Boolean, nullable=False),
                Column(
                    'date_created',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                ),
                Column('date_modified', DateTime)
            )
            return playlist


def date_created_update(context):
    """ A function that changes the format of a datetime """
    return datetime.datetime.strptime(
        context.current_parameters['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
    )


DATABASE = Database()
