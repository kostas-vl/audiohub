"""
Contains functions that load and manipulate settings
"""
import json
from configuration.server_settings import ServerSettings
from configuration.database_settings import DatabaseSettings
from configuration.backend_settings import BackendSettings
from configuration.youtube_settings import YoutubeSettings


class ApplicationSettings():
    """
    Contains static settings for the application
    """

    def __init__(self, settings_file='./settings.json'):
        self.settings_file_name = settings_file
        self.server = None
        self.database = None
        self.youtube = None
        self.backend = None

    def load(self):
        """
        A method that loads all the application settings from the settings file
        """
        try:
            with open(self.settings_file_name, 'r') as settings_file:
                content = settings_file.read()
                settings_dict = json.loads(content)
                self.server = ServerSettings(settings_dict['server'])
                self.database = DatabaseSettings(settings_dict['database'])
                self.youtube = YoutubeSettings(settings_dict['youtube'])
                self.backend = BackendSettings(settings_dict['backend'])
        except OSError as err:
            print('OS error: {0}'.format(err))


APP_SETTINGS_INSTANCE = ApplicationSettings()
