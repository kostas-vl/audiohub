""" Wrapper class on an mplayer slave process """
import sys
import subprocess
import configuration.application_settings as app_settings
from backends.backend_process import BackendProcess


class MplayerProcess(BackendProcess):
    """ A wrapper class for a mplayer process """

    def __execute(self, command):
        """ Executes the given command on a mplayer process """
        try:
            if self.process_handler is not None:
                command.append('\n')
                command_str = ' '.join(command)
                try:
                    self.process_handler.stdin.write(command_str)
                except (TypeError, UnicodeEncodeError):
                    self.process_handler.stdin.write(
                        command_str.encode('utf-8', 'ignore'))
                self.process_handler.stdin.flush()
        except OSError as err:
            print(err)
            if self.process_handler is not None:
                self.process_handler.terminate()
                self.process_handler = None

    def spawn(self):
        """ Spawns a new mplayer process """
        try:
            execution_path = ''
            if sys.platform == 'win32':
                execution_path = app_settings.INSTANCE.backend.win32_path
            else:
                execution_path = app_settings.INSTANCE.backend.linux_path
            self.process_handler = subprocess.Popen(
                [
                    execution_path,
                    '-slave',
                    '-slave',
                    '-idle',
                    '-really-quiet',
                    '-msglevel',
                    'global=4',
                    '-input',
                    'nodefault-bindings',
                    '-noconfig',
                    'all'
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                close_fds=(sys.platform != 'win32')
            )
        except OSError as err:
            print(err)
            if self.process_handler is not None:
                self.process_handler.terminate()
                self.process_handler = None
            return None

    def loadfile(self, file, append=False):
        """ Executes a command to load the provided file to the mplayer process """
        if self.process_handler is None:
            self.spawn()
        append_valid_value = str(int(append))
        self.__execute(['loadfile', "'" + file + "'", append_valid_value])

    def pause(self):
        """ Executes a command to pause the mplayer process """
        self.__execute(['pause'])

    def stop(self):
        """ Executes a command to stop the playback of the mplayer process """
        self.__execute(['stop'])

    def next(self):
        """ Executes a command to move to the next entry in the mplayer process """
        self.__execute(['pt_step', '1'])

    def previous(self):
        """ Executes a command to move to the previous entry in the mplayer process """
        self.__execute(['pt_step', '-1'])

    def seek(self, value, seek_type=None):
        """ Executes a command to seek a specific time in the playback of the mplayer proccess """
        str_seek_type = str(2 if seek_type is None else seek_type)
        self.__execute(['seek', str(value), str_seek_type])

    def time(self):
        """ Executes a command to get the length of the file in seconds """
        self.__execute(['get_time_length'])
        if self.process_handler is not None:
            try:
                if self.process_handler.stdout.readable():
                    result_bytes = self.process_handler.stdout.readline()
                    result_str = result_bytes.decode('utf-8')
                    seconds_str = result_str.replace('ANS_LENGTH=', '')
                    return float(seconds_str)
            except IOError:
                return None
        return None

    def current_time(self):
        """ Executes a command to get the current time on the playback of the player proccess """
        self.__execute(['get_time_pos'])        
        if self.process_handler is not None:
            try:
                if self.process_handler.stdout.readable():
                    result_bytes = self.process_handler.stdout.readline()
                    result_str = result_bytes.decode('utf-8')
                    seconds_str = result_str.replace('ANS_TIME_POSITION=', '')
                    return float(seconds_str)
            except IOError:
                return None
        return None

    def volume(self, value):
        """ Executes a command to set the volume of the mplayer process to the provided value """
        self.__execute(['volume', str(value), '1'])
