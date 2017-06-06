""" Wrapper functions on the mplayer """
import sys
import subprocess
import settings.container as settings


def execute(process, command):
    """ Executes the given command on a mplayer process """
    command.append('\n')
    command_str = ' '.join(command)
    try:
        process.stdin.write(command_str)
    except (TypeError, UnicodeEncodeError):
        process.stdin.write(command_str.encode('utf-8', 'ignore'))
    process.stdin.flush()
    return process


def spawn(file):
    """ Creates a new process for the mplayer """
    execution_path = ''
    if sys.platform == 'win32':
        execution_path = settings.MPLAYER['win32ExecutionPath']
    else:
        execution_path = settings.MPLAYER['linuxExecutionPath']
    return subprocess.Popen(
        [execution_path, '-slave', '-quiet', file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        close_fds=(sys.platform != 'win32')
    )


def loadfile(process, file, append=False):
    """ Executes a fileload command on a mplayer process """
    append_valid_value = str(int(append))
    return execute(process, ['loadfile', "'" + file + "'", append_valid_value])


def pause(process):
    """ Executes a pause command on a mplayer process """
    return execute(process, ['pause'])


def stop(process):
    """ Executes a stop command on a mplayer process """
    return execute(process, ['stop'])


def seek(process, value, seek_type):
    """ Executes a seek command on a mplayer process """
    return execute(process, ['seek', str(value), str(seek_type)])


def volume(process, value):
    """ Executes a volume command on a mplayer process """
    return execute(process, ['volume', str(value), '1'])
