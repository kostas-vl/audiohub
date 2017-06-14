""" Wrapper class on an mplayer slave process """
import sys
import subprocess
import settings.container as settings


class MplayerProcess():
    """ A wrapper class for a mplayer process """

    def __init__(self):
        self.__process = None

    def __del__(self):
        if self.__process is None:
            self.__process.terminate()

    def __execute(self, command):
        """ Executes the given command on a mplayer process """
        if self.__process is not None:
            command.append('\n')
            command_str = ' '.join(command)
            try:
                self.__process.stdin.write(command_str)
            except (TypeError, UnicodeEncodeError):
                self.__process.stdin.write(
                    command_str.encode('utf-8', 'ignore'))
            self.__process.stdin.flush()

    def spawn(self):
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

    def loadfile(self, file, append=False):
        """ Executes a fileload command on a mplayer process """
        try:
            if self.__process is None:
                self.spawn()
            # else:
            append_valid_value = str(int(append))
            self.__execute(['loadfile', "'" + file + "'", append_valid_value])
        except OSError:
            if self.__process is not None:
                self.__process.terminate()
                self.__process = None

    def pause(self):
        """ Executes a pause command on a mplayer process """
        try:
            self.__execute(['pause'])
        except OSError:
            if self.__process is not None:
                self.__process.terminate()
                self.__process = None

    def stop(self):
        """ Executes a stop command on a mplayer process """
        try:
            self.__execute(['stop'])
        except OSError:
            if self.__process is not None:
                self.__process.terminate()
                self.__process = None

    def next(self):
        """ Executes a next command on a mplayer process """
        try:
            self.__execute(['pt_step', '1'])
        except OSError:
            if self.__process is not None:
                self.__process.terminate()
                self.__process = None

    def previous(self):
        """ Executes a previous command on a mplayer process """
        try:
            self.__execute(['pt_step', '-1'])
        except OSError:
            if self.__process is not None:
                self.__process.terminate()
                self.__process = None

    def seek(self, value, seek_type):
        """ Executes a seek command on a mplayer process """
        try:
            self.__execute(['seek', str(value), str(seek_type)])
        except OSError:
            if self.__process is not None:
                self.__process.terminate()
                self.__process = None

    def volume(self, value):
        """ Executes a volume command on a mplayer process """
        try:
            self.__execute(['volume', str(value), '1'])
        except OSError:
            if self.__process is not None:
                self.__process.terminate()
                self.__process = None
