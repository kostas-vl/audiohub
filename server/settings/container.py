""" Contains functions that load and manipulate settings """
import json

SETTINGS_FILE_NAME = './settings.json'

DATABASE = None
MPLAYER = None

def load():
    """ Loads the application settings based on the registered file path """
    global DATABASE, MPLAYER
    try:
        with open(SETTINGS_FILE_NAME, 'r') as settings_file:
            content = settings_file.read()
            settings_dict = json.loads(content)
            DATABASE = settings_dict['database']
            MPLAYER = settings_dict['mplayer']
    except OSError as err:
        print('OS error: {0}'.format(err))
