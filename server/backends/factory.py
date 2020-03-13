"""
Module that contains various function for constructing a backend.
"""
import backends.mplayer_process as mpl
import backends.mpv_process as mpv


def create_backend(config):
    """
    A function that initiates a process wrapper based on the provided
    configuration
    """
    wrapper_name = config.name
    if wrapper_name == 'mplayer':
        return mpl.MplayerProcess()
    if wrapper_name == 'mpv':
        return mpv.MpvProcess()
    return None
