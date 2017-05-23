""" Contains event handlers for manipulating the player """
import enum
import collections
import pygame as pg
import sound.playlist as pl
from flask_socketio import emit
from enviroment import SOCKET_IO


class PlayerState(enum.Enum):
    """ Enum that shows various player state values """
    Init = 'init'
    Stoped = 'stoped'
    Paused = 'paused'
    Playing = 'playling'


class Player():
    """ Class that implements a basic music player """

    def __init__(self):
        self.current_track = None
        self.state = PlayerState.Init
        if not pg.mixer.get_init():
            pg.mixer.init(44100)

    def add(self, entry):
        if entry is not None:
            playlist = pl.Playlist(entry)
            playlist.active = True
            pl.insert(playlist)

    def remove(self, id):
        if id is not None:
            playlist = pl.select_by_id(id)
            playlist.active = False
            pl.delete_by_id(id)

    def remove_all(self):
        pl.delete_all()

    def play(self, track=None):
        if self.state == PlayerState.Paused or self.state == PlayerState.Stoped:
            pg.mixer.music.unpause()
            self.state = PlayerState.Playing
        elif self.state == PlayerState.Init and track is None:
            playlist = pl.select_active()
            if playlist:
                pg.mixer.music.load(playlist.pop())
                self.state = PlayerState.Playing
        elif track is not None:
            pg.mixer.music.load(track.path)
            pg.mixer.music.play()
            self.state = PlayerState.Playing

    def play_all(self):
        if self.state == PlayerState.Paused or self.state == PlayerState.Playing:
            self.stop()
            self.state = PlayerState.Stoped
        playlist = pl.select_active()
        if playlist and isinstance(playlist, collections.Sequence):
            for entry in playlist:
                pg.mixer.music.queue(entry.path)
        pg.mixer.music.play()
        self.state = PlayerState.Playing

    def pause(self):
        if self.state == PlayerState.Playing:
            pg.mixer.music.pause()
            self.state = PlayerState.Paused

    def stop(self):
        if self.state == PlayerState.Playing or self.state == PlayerState.Paused:
            pg.mixer.music.rewind()
            self.pause()
            self.state = PlayerState.Stoped

    def next(self):
        pass

    def previous(self):
        pass

    def volume(self, value):
        pg.mixer.music.set_volume(value)

    def has_entries(self):
        playlist = pl.select_active()
        return playlist and isinstance(playlist, collections.Sequence)



# audio player initialization and configuration
AUDIO_PLAYER = Player()


def currently_playling(entry):
    """ A function that sends the entry that is currently playing """
    emit('currently playing', dict(entry))


def emit_queue():
    """ A functions that sends the currently active tracks """
    emit('queue', [dict(entry) for entry in pl.select_active()])


@SOCKET_IO.on('play', namespace='/server')
def play_audio(data):
    """ A function that starts playing the first track on the playlist """
    AUDIO_PLAYER.play()


@SOCKET_IO.on('play now', namespace='/server')
def play_now(data):
    """ A function that plays the track that is provided removing
        every source queued up until now
    """
    entries = pl.select_active_by_path(data['path'])
    # if there are entries, the first entry is queued and the the audio player
    # start playing
    if isinstance(entries, collections.Sequence) and entries:
        track = entries[0]
        AUDIO_PLAYER.play(track)
        currently_playling(track)


@SOCKET_IO.on('play all', namespace='/server')
def play_all(data):
    """ A function that plays all the active entries in the playlist table """
    # gets all the active entries in the playlsit table
    playlist = pl.select_active()
    if isinstance(playlist, collections.Sequence) and playlist:
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
    # AUDIO_PLAYER.pause()
    # AUDIO_PLAYER.seek(0)
    AUDIO_PLAYER.stop()


@SOCKET_IO.on('next', namespace='/server')
def next_track(data):
    """ starts playing the next track in the queue """
    AUDIO_PLAYER.next()
    # AUDIO_PLAYER.next_source()
    # source = AUDIO_PLAYER.source
    # if source is not None:
    #     print(source)


@SOCKET_IO.on('volume', namespace='/server')
def volume_audio(data):
    """ event handler for controlling the volume of the audio player """
    # AUDIO_PLAYER.volume = data / 100
    AUDIO_PLAYER.volume(data / 100)


@SOCKET_IO.on('queue push', namespace='/server')
def queue_push(entry):
    """ event handler for pushing a new track on the queue """
    AUDIO_PLAYER.add(entry)
    emit_queue()


@SOCKET_IO.on('queue pop', namespace='/server')
def queue_pop(data):
    """ event handler for poping a track from queue """
    AUDIO_PLAYER.remove(data)
    emit_queue()


@SOCKET_IO.on('queue', namespace='/server')
def queue(data):
    """ List queued tracks event handler """
    emit_queue()
