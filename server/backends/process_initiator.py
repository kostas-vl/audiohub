""" Contains a functions that initiates a backend process wrapper """
import backends.mplayer_process as mpl
import backends.mpv_process as mpv

def process_wrapper_init(config):
    """ A function that initiates a process wrapper based on the provided configuration """
    wrapper_name = config.name
    if wrapper_name == 'mplayer':
        return mpl.MplayerProcess()
    elif wrapper_name == 'mpv':
        return mpv.MpvProcess
    else:
        return None
