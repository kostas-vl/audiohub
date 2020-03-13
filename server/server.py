"""
The initial file of the application
"""
import os
import endpoints.download
import endpoints.files
import endpoints.player
import endpoints.server
import endpoints.settings
import models.users
import models.user_settings
import models.file_system
import models.playlist
from configuration import APP_SETTINGS_INSTANCE
from sound import PLAYER_INSTANCE
from flask_socketio import join_room, leave_room, emit
from database import DATABASE_INSTANCE
from enviroment import SOCKET_IO, APP


def main():
    """
    The main source of the application execution
    """
    print('Loading settings...')
    APP_SETTINGS_INSTANCE.load()

    print('Initializing player instance...')
    PLAYER_INSTANCE.init()

    print('Initializing database schema image...')
    DATABASE_INSTANCE.init(APP_SETTINGS_INSTANCE.database)

    print('Starting the flask socket-io server...')
    APP.config['SECRET'] = APP_SETTINGS_INSTANCE.server.secret
    SOCKET_IO.run(
        APP,
        host=os.getenv('IP', APP_SETTINGS_INSTANCE.server.ip_address),
        port=int(os.getenv('PORT', int(APP_SETTINGS_INSTANCE.server.port))),
        debug=True
    )


if __name__ == '__main__':
    main()
