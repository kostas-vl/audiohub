"""
Wrapper class on an mpv process
"""
import sys
import subprocess
import configuration.application_settings as app_settings
from backends.backend_process import BackendProcess


class MpvProcess(BackendProcess):
    """
    A wrapper class for a mpv process
    """

    def __execute(self, command):
        """
        Executes the given command on the mpv process
        """
        raise NotImplementedError
