"""
Contains functions that load and manipulate settings
"""
import os
import sys
import json


class BaseSettings():
    """
    Contains base methods for the applcation settings
    """

    def init_from_dict(self, args):
        """
        Initializes the classes attributes based on the content of the provided dictionary
        """
        for dictionary in args:
            for key in dictionary:
                if hasattr(self, key):
                    setattr(self, key, dictionary[key])


class ServerSettings(BaseSettings):
    """
    Contains static information for the server options
    """

    def __init__(self, *initargs):
        self.ip_address = None
        self.port = None
        self.secret = None
        self.allowed_origins = None
        self.init_from_dict(initargs)


class DatabaseSettings(BaseSettings):
    """
    Contains static information for the database options
    """

    def __init__(self, *initargs):
        self.connection_string = None
        self.echo = None
        self.init_from_dict(initargs)


class YoutubeSettings(BaseSettings):
    """
    Contains static information for the youtube-dl options
    """

    def __init__(self, *initargs):
        self.win32_path = None
        self.linux_path = None
        self.init_from_dict(initargs)


class BackendSettings(BaseSettings):
    """
    Contains static information for the backend player options
    """

    def __init__(self, backends):
        self.name = None
        self.win32_path = None
        self.linux_path = None
        # Loop the provided backends
        for entry in backends:
            try:
                # Apply the settings
                self.init_from_dict([entry])
                # Apply a validation method
                check_platform_access = None
                if sys.platform == 'win32':
                    check_platform_access = self.__check_win32_access
                elif sys.platform == 'linux':
                    check_platform_access = self.__check_linux_access
                else:
                    raise NameError()
                # Check the availability of the backend on the current platform
                is_accessible = check_platform_access()
                if is_accessible:
                    break
                else:
                    self.__reset_attrs()
                    continue
            except NameError:
                self.__reset_attrs()
                break

    def __reset_attrs(self):
        """
        A method that resets the values of the attributes
        """
        self.name = None
        self.win32_path = None
        self.linux_path = None

    def __check_win32_access(self):
        """
        A method that checks if the specified backend is accessible
        in the current windows platform
        """
        return os.path.isfile(self.win32_path) and os.access(self.win32_path, os.X_OK)

    def __check_linux_access(self):
        """
        A method that checks if the specified backend is accessible
        in the current linux platform
        """
        return os.path.isfile(self.linux_path) and os.access(self.linux_path, os.X_OK)


class AppSettings():
    """
    Contains static settings for the application
    """

    def __init__(self):
        self.settings_file_name = './settings.json'
        self.server = None
        self.database = None
        self.youtube = None
        self.backend = None

    def load(self):
        """
        A method that loads all the application settings from the settings file
        """
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
                # Assign the youtube-dl settings
                self.youtube = YoutubeSettings(settings_dict['youtube'])
                # Assign the backend settings
                self.backend = BackendSettings(settings_dict['backend'])
        except OSError as err:
            print('OS error: {0}'.format(err))


INSTANCE = AppSettings()
