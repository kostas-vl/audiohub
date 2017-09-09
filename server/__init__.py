"""
The initialization file of the server module
"""
import models.users
import models.user_settings
import models.file_system
import models.playlist
import configuration.application_settings
import configuration.settings
import sound.player
import drive.files
import drive.download
import database.schema
import enviroment
import program

if __name__ == '__main__':
    program.main()
