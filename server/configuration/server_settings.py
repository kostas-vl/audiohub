"""
Module that exposes the ServerSettings class.
"""
from configuration.base_settings import BaseSettings


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
