""" Contains functions that load and manipulate settings """
import json


class BaseSettings():
    """ Contains base methods for the applcation settings """

    def init_from_dict(self, args):
        """ Initializes the classes attributes based on the content of the provided dictionary """
        for dictionary in args:
            for key in dictionary:
                if hasattr(self, key):
                    setattr(self, key, dictionary[key])


class ServerSettings(BaseSettings):
    """ Contains static information for the server options """

    def __init__(self, *initargs):
        self.ip_address = None
        self.port = None
        self.init_from_dict(initargs)


class DatabaseSettings(BaseSettings):
    """ Contains static information for the database options """

    def __init__(self, *initargs):
        self.connection_string = None
        self.echo = None
        self.init_from_dict(initargs)


class MplayerSettings(BaseSettings):
    """ Contains static information for the mplayer options """

    def __init__(self, *initargs):
        self.win32_path = None
        self.linux_path = None
        self.init_from_dict(initargs)


class YoutubeSettings(BaseSettings):
    """ Contains static information for the youtube-dl options """

    def __init__(self, *initargs):
        self.win32_path = None
        self.linux_path = None
        self.init_from_dict(initargs)


class AppSettings():
    """ Contains static settings for the application """

    def __init__(self):
        self.settings_file_name = './settings.json'
        self.server = None
        self.database = None
        self.mplayer = None
        self.youtube = None

    def load(self):
        """ A method that loads all the application settings from the settings file """
        try:
            # Opening the settings file
            with open(self.settings_file_name, 'r') as settings_file:
                # Reed the content and laod it in a dictionary
                content = settings_file.read()
                settings_dict = json.loads(content)
                # Assign the server settings
                self.server = ServerSettings(settings_dict['server'])
                # Assign the database settings
                self.database = DatabaseSettings(settings_dict['database'])
                # Assign the mplayer settings
                self.mplayer = MplayerSettings(settings_dict['mplayer'])
                # Assign the youtube-dl settings
                self.youtube = YoutubeSettings(settings_dict['youtube'])
        except OSError as err:
            print('OS error: {0}'.format(err))


INSTANCE = AppSettings()
