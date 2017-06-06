""" Wrapper functions on the mplayer """
import sys
import subprocess
import settings.container as settings


class MplayerProcess():
    """ A wrapper class for a mplayer process """

    def __init__(self, file):
        self.__process = None
        self.spawn(file)

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

# def execute(process, command):
#     """ Executes the given command on a mplayer process """
#     command.append('\n')
#     command_str = ' '.join(command)
#     try:
#         process.stdin.write(command_str)
#     except (TypeError, UnicodeEncodeError):
#         process.stdin.write(command_str.encode('utf-8', 'ignore'))
#     process.stdin.flush()
#     return process


# def spawn(file):
#     """ Creates a new process for the mplayer """
#     execution_path = ''
#     if sys.platform == 'win32':
#         execution_path = settings.MPLAYER['win32ExecutionPath']
#     else:
#         execution_path = settings.MPLAYER['linuxExecutionPath']
#     return subprocess.Popen(
#         [execution_path, '-slave', '-quiet', file],
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         close_fds=(sys.platform != 'win32')
#     )


# def loadfile(process, file, append=False):
#     """ Executes a fileload command on a mplayer process """
#     append_valid_value = str(int(append))
# return execute(process, ['loadfile', "'" + file + "'",
# append_valid_value])


# def pause(process):
#     """ Executes a pause command on a mplayer process """
#     return execute(process, ['pause'])


# def stop(process):
#     """ Executes a stop command on a mplayer process """
#     return execute(process, ['stop'])


# def seek(process, value, seek_type):
#     """ Executes a seek command on a mplayer process """
#     return execute(process, ['seek', str(value), str(seek_type)])


# def volume(process, value):
#     """ Executes a volume command on a mplayer process """
#     return execute(process, ['volume', str(value), '1'])
