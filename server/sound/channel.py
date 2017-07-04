""" Contains event for streaming audio files to client """
import os
import collections
import models.playlist as pl
from pydub import AudioSegment
from enviroment import SOCKET_IO, emit


def get_raw_data(path):
    """ Returns the bytes of the audio file in the provided path """
    if os.path.isfile(path):
        _, ext = os.path.splitext(path)
        if ext == '.wav':
            song = AudioSegment.from_wav(path)
            return song.raw_data
        elif ext == '.mp3':
            song = AudioSegment.from_mp3(path)
            return song.raw_data
        else:
            return None
    else:
        return None


@SOCKET_IO.on('channel stream', namespace='/server')
def on_channel_stream(data):
    """ Stream audio file to client """
    if data:
        playlist = pl.select_by_path(data['path'])
        if isinstance(playlist, collections.Sequence) and playlist:
            details = playlist[0]
            raw_data = get_raw_data(details.path)
            if raw_data:
                emit('channel stream', raw_data)
