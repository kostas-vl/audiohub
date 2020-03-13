"""
Module that exposes the DatabaseSettings class.
"""
from configuration.base_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """
    Contains static information for the database options
    """

    def __init__(self, *initargs):
        self.connection_string = None
        self.echo = None
        self.init_from_dict(initargs)
