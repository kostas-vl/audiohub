""" Contains functions that initialize the database schema """
import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, Boolean, MetaData, create_engine, select, delete, bindparam, func


class Database():
    """ Class representing the database and the database schema """

    def __init__(self):
        self.engine = None
        self.metadata = None
        self.users = None
        self.user_settings = None
        self.file_systems = None
        self.playlist = None
        self.connection_string = None

    def init(self, database_settings):
        """ A function that initializes the apps database """
        # Get the database connection options from the settings
        self.connection_string = database_settings['connectionString']
        echo = database_settings['echo']
        if self.connection_string:
            # Initializing the database engine and nmetadata
            self.engine = create_engine(self.connection_string, echo=echo)
            self.metadata = MetaData()
            # Initializing the database tables
            self.users = self.users_init()
            self.user_settings = self.user_settings_init()
            self.file_systems = self.file_systems_init()
            self.playlist = self.playlist_init()
            # Create the tables
            self.metadata.create_all(self.engine)
        else:
            raise NameError('Database Connection String not found!')

    def file_systems_init(self):
        """ A method that initialized the file_systems table """
        if self.engine and self.metadata:
            systems = Table(
                'file_systems',
                self.metadata,
                Column('identity', Integer, primary_key=True),
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
                Column(
                    'date_modified',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                )
            )
            return systems

    def playlist_init(self):
        """ A method that intializes the playlist table """
        if self.engine and self.metadata:
            playlist = Table(
                'playlist',
                self.metadata,
                Column('identity', Integer, primary_key=True),
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
                Column(
                    'date_modified',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                )
            )
            return playlist

    def users_init(self):
        """ A method taht initializes the users table """
        if self.engine and self.metadata:
            users = Table(
                'users',
                self.metadata,
                Column('identity', Integer, primary_key=True),
                Column('user_ip', String, nullable=False),
                Column('session_id', String, nullable=False),
                Column('active', Boolean, nullable=False),
                Column(
                    'date_created',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                ),
                Column(
                    'date_modified',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                )
            )
            return users

    def user_settings_init(self):
        """ A method that initializes the user details table """
        if self.engine and self.metadata:
            user_settings = Table(
                'user_settings',
                self.metadata,
                Column('identity', Integer, primary_key=True),
                Column('user_id', Integer, nullable=False),
                Column('sound_direction', String, nullable=False),
                Column('dark_theme', Boolean, nullable=False),
                Column('sidenav_mode', String, nullable=False),
                Column(
                    'date_created',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                ),
                Column(
                    'date_modified',
                    DateTime,
                    nullable=False,
                    onupdate=date_created_update
                )
            )
            return user_settings


def date_created_update(context):
    """ A function that changes the format of a datetime """
    return datetime.datetime.strptime(
        context.current_parameters['date_created'], '%Y-%m-%dT%H:%M:%S.%f'
    )


DATABASE = Database()
