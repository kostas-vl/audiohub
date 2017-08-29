"""
Base class for the various implementations of music player backends
"""


class BackendProcess():
    """
    A base class for a music player process wrapper
    """

    def __init__(self):
        self.process_handler = None

    def __del__(self):
        if self.process_handler is not None:
            self.process_handler.terminate()

    def spawn(self):
        """
        Spawns a new player process
        """
        raise NotImplementedError()

    def loadfile(self, file, append=False):
        """
        Executes a command to load the provided file to the player process
        """
        raise NotImplementedError()

    def pause(self):
        """
        Executes a command to pause the player process
        """
        raise NotImplementedError()

    def stop(self):
        """
        Executes a command to stop the playback of the player process
        """
        raise NotImplementedError()

    def next(self):
        """
        Executes a command to move to the next entry in the player process
        """
        raise NotImplementedError()

    def previous(self):
        """
        Executes a command to move to the previous entry in the player process
        """
        raise NotImplementedError()

    def seek(self, value, seek_type=None):
        """
        Executes a command to seek a specific time in the playback of the player proccess
        """
        raise NotImplementedError()

    def time(self):
        """
        Executes a command to get the length of the file in seconds
        """
        raise NotImplementedError()

    def current_time(self):
        """
        Executes a command to get the current time on the playback of the player proccess
        """
        raise NotImplementedError()

    def volume(self, value):
        """
        Executes a command to set the volume of the player process to the provided value
        """
        raise NotImplementedError()
