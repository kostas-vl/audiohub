"""
Module that exposes the BaseSettings class.
"""


class BaseSettings():
    """
    Contains base methods for the applcation settings
    """

    def init_from_dict(self, args):
        """
        Initializes the classes attributes based on the content of
        the provided dictionary
        """
        for dictionary in args:
            for key in dictionary:
                if hasattr(self, key):
                    setattr(self, key, dictionary[key])
