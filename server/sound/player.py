""" Contains event handlers for manipulating the player """
import collections
import pyglet
import sound.playlist as pl
from flask_socketio import emit
from enviroment import SOCKET_IO

# audio player initialization and configuration
AUDIO_PLAYER = pyglet.media.Player()


def currently_playling(entry):
    """ A function that sends the entry that is currently playing """
    emit('currently playing', dict(entry))


def emit_queue():
    """ A functions that sends the currently active tracks """
    emit('queue', [dict(entry) for entry in pl.select_active()])


@SOCKET_IO.on('play', namespace='/server')
def play_audio(data):
    """ A function that starts playing the first track on the playlist """
    if AUDIO_PLAYER.source is None and not AUDIO_PLAYER.playing:
        playlist_collection = pl.select_active()
        source = pyglet.media.load(playlist_collection[0].path)
        AUDIO_PLAYER.queue(source)

    if not AUDIO_PLAYER.playing:
        AUDIO_PLAYER.play()
        currently_playling(playlist_collection[0])


@SOCKET_IO.on('play now', namespace='/server')
def play_now(data):
    """ A function that plays the track that is provided removing
        every source queued up until now
    """
    while AUDIO_PLAYER.source is not None:
        AUDIO_PLAYER.next_source()

    # getting all the active entries with the provided path
    entries = pl.select_active_by_path(data['path'])

    # if there are entries, the first entry is queued and the the audio player
    # start playing
    if isinstance(entries, collections.Sequence) and entries:
        track = entries[0]
        source = pyglet.media.load(track.path)
        AUDIO_PLAYER.queue(source)
        AUDIO_PLAYER.play()
        currently_playling(track)


@SOCKET_IO.on('play all', namespace='/server')
def play_all(data):
    """ A function that plays all the active entries in the playlist table """
    # pauses the audio player
    if AUDIO_PLAYER.playing:
        AUDIO_PLAYER.pause()

    # removes all the source currently queued
    while AUDIO_PLAYER.source is not None:
        AUDIO_PLAYER.next_source()

    # gets all the active entries in the playlsit table
    playlist = pl.select_active()
    if isinstance(playlist, collections.Sequence) and playlist:
        # queue all the entries available
        for track in playlist:
            source = pyglet.media.load(track.path)
            AUDIO_PLAYER.queue(source)

        # start playing and emit the current track
        AUDIO_PLAYER.play()
        currently_playling(playlist[0])


@SOCKET_IO.on('pause', namespace='/server')
def pause_audio(data):
    """ event handler for pausing the audio player """
    AUDIO_PLAYER.pause()


@SOCKET_IO.on('stop', namespace='/server')
def stop_audio(data):
    """ event handler for stoping the audio player """
    AUDIO_PLAYER.pause()
    AUDIO_PLAYER.seek(0)


@SOCKET_IO.on('next', namespace='/server')
def next_track(data):
    """ starts playing the next track in the queue """
    AUDIO_PLAYER.next_source()
    source = AUDIO_PLAYER.source
    if source is not None:
        print(source)


@SOCKET_IO.on('volume', namespace='/server')
def volume_audio(data):
    """ event handler for controlling the volume of the audio player """
    AUDIO_PLAYER.volume = data / 100


@SOCKET_IO.on('queue push', namespace='/server')
def queue_push(entry):
    """ event handler for pushing a new track on the queue """
    playlist = pl.Playlist(entry)
    playlist.active = True
    pl.insert(playlist)
    emit_queue()


@SOCKET_IO.on('queue pop', namespace='/server')
def queue_pop(data):
    """ event handler for poping a track from queue """
    playlist = pl.select_by_id(data)
    playlist.active = False
    pl.update_by_id(playlist)
    emit_queue()


@SOCKET_IO.on('queue', namespace='/server')
def queue(data):
    """ List queued tracks event handler """
    emit_queue()
