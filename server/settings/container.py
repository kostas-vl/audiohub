""" Contains functions that load and manipulate settings """
import json

SETTINGS_FILE_NAME = './settings.json'
DATABASE_SETTINGS = None

def load():
    """ Loads the application settings based on the registered file path """
    global DATABASE_SETTINGS
    try:
        with open(SETTINGS_FILE_NAME, 'r') as settings_file:
            content = settings_file.read()
            settings_dict = json.loads(content)
            DATABASE_SETTINGS = settings_dict['database']
    except OSError as err:
        print('OS error: {0}'.format(err))
