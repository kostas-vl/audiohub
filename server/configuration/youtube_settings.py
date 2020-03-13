"""
Module that exposes the YoutubeSettings class.
"""
from configuration.base_settings import BaseSettings


class YoutubeSettings(BaseSettings):
    """
    Contains static information for the youtube-dl options
    """

    def __init__(self, *initargs):
        self.win32_path = None
        self.linux_path = None
        self.init_from_dict(initargs)
