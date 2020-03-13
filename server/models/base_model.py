"""
Module that exposes the BaseModel class.
"""


class BaseModel():
    """
    The base class for the models of the application
    """

    def init_from_dict(self, data):
        """
        Loop the data dictionary and assign the values to attributes
        """
        for dictionary in data:
            for key in dictionary:
                if hasattr(self, key):
                    setattr(self, key, dictionary[key])

    def init_from_kwords(self, kwords):
        """
        Loop the key words provided and assign the values
        """
        for key in kwords:
            if hasattr(self, key):
                setattr(self, key, kwords[key])
