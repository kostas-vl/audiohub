""" Wrapper class on an mplayer slave process """
import sys
import subprocess
import settings.container as settings


class MplayerProcess():
    """ A wrapper class for a mplayer process """

    def __init__(self):
        self.__process = None

    def __execute(self, command):
        """ Executes the given command on a mplayer process """
        command.append('\n')
        command_str = ' '.join(command)
        try:
            self.__process.stdin.write(command_str)
        except (TypeError, UnicodeEncodeError):
            self.__process.stdin.write(command_str.encode('utf-8', 'ignore'))
        self.__process.stdin.flush()

    def spawn(self, file):
        """ Spawns a new mplayer process """
        execution_path = ''
        if sys.platform == 'win32':
            execution_path = settings.MPLAYER['win32ExecutionPath']
        else:
            execution_path = settings.MPLAYER['linuxExecutionPath']
        self.__process = subprocess.Popen(
            [
                execution_path,
                '-slave',
                '-quiet',
                file
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            close_fds=(sys.platform != 'win32')
        )

    def loadfile(self, file, append=False):
        """ Executes a fileload command on a mplayer process """
        try:
            if self.__process is None:
                self.spawn(file)
            else:
                append_valid_value = str(int(append))
                self.__execute(['loadfile', "'" + file + "'", append_valid_value])
        except OSError:
            self.__process.terminate()
            self.spawn(file)

    def pause(self):
        """ Executes a pause command on a mplayer process """
        try:
            self.__execute(['pause'])
        except OSError:
            pass

    def stop(self):
        """ Executes a stop command on a mplayer process """
        try:
            self.__execute(['stop'])
        except OSError:
            pass

    def seek(self, value, seek_type):
        """ Executes a seek command on a mplayer process """
        try:
            self.__execute(['seek', str(value), str(seek_type)])
        except OSError:
            pass

    def volume(self, value):
        """ Executes a volume command on a mplayer process """
        try:
            self.__execute(['volume', str(value), '1'])
        except OSError:
            pass
