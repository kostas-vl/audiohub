"""
Module that exposes the BackendSettings class.
"""
import os
import sys
from configuration.base_settings import BaseSettings


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
            except NameError as e:
                self.__reset_attrs()
                print(e)
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
        return (
            os.path.isfile(self.win32_path)
            and os.access(self.win32_path, os.X_OK)
        )

    def __check_linux_access(self):
        """
        A method that checks if the specified backend is accessible
        in the current linux platform
        """
        return (
            os.path.isfile(self.linux_path)
            and os.access(self.linux_path, os.X_OK)
        )
