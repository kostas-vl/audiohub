"""
Module that exposes the network file system class.
"""
from models.base_model import BaseModel


class NetworkFileSystem(BaseModel):
    """
    Class representing a network file system details
    """

    def __init__(self, *initial_data, **kwords):
        self.ip_address = ''
        self.directory = ''
        self.user = ''
        self.password = ''
        self.persistent = True
        self.init_from_dict(initial_data)
        self.init_from_kwords(kwords)

    def __iter__(self):
        yield 'ip', self.ip_address
        yield 'directory', self.directory
        yield 'user', self.user
        yield 'password', self.password
        yield 'persistent', self.persistent
