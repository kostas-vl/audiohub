import sys
import json

settings_file_name = './settings.json'

database_settings = None

def load():
    global database_settings
    try:
        with open(settings_file_name, 'r') as settings_file:
            content = settings_file.read()
            settings_dict = json.loads(content)            
            database_settings = settings_dict['database']
    except OSError as err:
        print('OS error: {0}'.format(err))