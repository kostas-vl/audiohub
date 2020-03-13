"""
This module contains all the player endpoints.
"""
import collections
import models.playlist as playlist
import models.streams as streams
from sound import PLAYER_INSTANCE
from enviroment import SOCKET_IO
from flask_socketio import emit


@SOCKET_IO.on('player info', namespace='/server')
def on_player_info(_):
    """
    A function that sends the info of the player
    """
    info = dict(PLAYER_INSTANCE.info)
    emit('player info', info, broadcast=True)


@SOCKET_IO.on('play', namespace='/server')
def on_play(data):
    """
    A function that plays the track that is provided removing
    every source queued up until now
    """
    if data:
        entries = playlist.select_active_by_path(data['path'])
        if isinstance(entries, collections.Sequence) and entries:
            track = entries[0]
            PLAYER_INSTANCE.play(track)
            on_player_info(None)
    else:
        PLAYER_INSTANCE.play()
        on_player_info(None)


@SOCKET_IO.on('play all', namespace='/server')
def on_play_all(_):
    """
    A function that plays all the active entries in the playlist table
    """
    active_playlist = playlist.select_active()
    if isinstance(active_playlist, collections.Sequence) and active_playlist:
        PLAYER_INSTANCE.play(playlist)
        on_player_info(None)


@SOCKET_IO.on('pause', namespace='/server')
def on_pause(_):
    """
    Event handler for pausing the audio player
    """
    PLAYER_INSTANCE.pause()
    on_player_info(None)


@SOCKET_IO.on('stop', namespace='/server')
def on_stop(_):
    """
    Event handler for stoping the audio player
    """
    PLAYER_INSTANCE.stop()
    on_player_info(None)


@SOCKET_IO.on('previous', namespace='/server')
def on_previous(_):
    """
    Starts playing the previous track in the queue
    """
    PLAYER_INSTANCE.previous()
    on_player_info(None)


@SOCKET_IO.on('next', namespace='/server')
def on_next(_):
    """
    Starts playing the next track in the queue
    """
    PLAYER_INSTANCE.next()
    on_player_info(None)


@SOCKET_IO.on('volume', namespace='/server')
def on_volume(data):
    """
    Event handler for controlling the volume of the audio player
    """
    PLAYER_INSTANCE.volume(data)
    on_player_info(None)


@SOCKET_IO.on('current time', namespace='/server')
def on_current_time(_):
    """
    Event handler for fetching the current time on the audio player
    """
    time, time_str = PLAYER_INSTANCE.current_time()
    emit('current time', {'currentTime': time, 'currentTimeStr': time_str})


@SOCKET_IO.on('queue push', namespace='/server')
def on_queue_push(data):
    """
    Event handler for pushing a new track on the queue
    """
    PLAYER_INSTANCE.add(data)
    on_player_info(None)
    on_queue(None)


@SOCKET_IO.on('queue pop', namespace='/server')
def on_queue_pop(data):
    """
    Event handler for poping a track from queue
    """
    PLAYER_INSTANCE.remove(data)
    on_player_info(None)
    on_queue(None)


@SOCKET_IO.on('queue', namespace='/server')
def on_queue(_):
    """
    List queued tracks event handler
    """
    try:
        emit('queue', [dict(entry) for entry in playlist.select_active()])
    except Exception as err:
        print(err)
        raise err


@SOCKET_IO.on('stream history', namespace='/server')
def on_stream_history(_):
    """
    List all registered streams
    """
    try:
        emit('stream history', [dict(entry) for entry in streams.select()])
    except Exception as err:
        print(err)
        raise err


@SOCKET_IO.on('load stream', namespace='/server')
def on_load_stream(url):
    """
    Load an incoming stream to mplayer
    """
    if url:
        PLAYER_INSTANCE.load_stream(url)
        on_player_info(None)
        emit('load stream complete')
        on_stream_history(None)
