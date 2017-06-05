""" Contains event handlers for manipulating the player """
import sys
import subprocess
import collections
import enum
import pygame as pg
import sound.playlist as pl
from flask_socketio import emit
from enviroment import SOCKET_IO


class PlayerStateEnum(enum.Enum):
    """ Enum that shows various player state values """
    Init = 'init'
    Stoped = 'stoped'
    Paused = 'paused'
    Playing = 'playing'


class PlayerInfo():
    """ Class that holds information about a music player """

    def __init__(self):
        self.track = ''
        self.volume = 100
        self.state = PlayerStateEnum.Init

    def __iter__(self):
        yield 'track', dict(self.track)
        yield 'volume', self.volume
        yield 'state', self.state.value


class MPlayer():
    """ Class that interops with the mplayer """

    def __init__(self):
        self.info = PlayerInfo()
        self.mplayer_process = None

    def add(self, entry):
        """ Adds a new entry on the playlist """
        if entry is not None:
            playlist = pl.Playlist(entry)
            playlist.active = True
            pl.insert(playlist)

    def remove(self, id):
        """ A method that removes an entry from the playlist based on the provided id """
        if id is not None:
            playlist = pl.select_by_id(id)
            playlist.active = False
            pl.delete_by_id(id)

    def remove_all(self):
        """ A method that removes all entries from the playlist """
        pl.delete_all()

    def play(self, track=None):
        """ A method that plays music based on the state of the player """
        if (
                (
                    self.info.state == PlayerStateEnum.Paused or
                    self.info.state == PlayerStateEnum.Stoped
                ) and
                track is None
        ):
            command = ' '.join(['pause', '\n'])
            try:
                self.mplayer_process.stdin.write(command)
            except (TypeError, UnicodeEncodeError):
                self.mplayer_process.stdin.write(command.encode('utf-8', 'ignore'))
            self.mplayer_process.stdin.flush()
            self.info.state = PlayerStateEnum.Playing

        elif self.info.state == PlayerStateEnum.Init and track is None:
            playlist = pl.select_active()
            if playlist:
                track = playlist.pop(0)
                pg.mixer.music.load(track.path)
                self.info.track = track
                self.info.state = PlayerStateEnum.Playing
                pg.mixer.music.play()

        elif track is not None:
            self.info.track = track
            self.info.state = PlayerStateEnum.Playing
            if self.mplayer_process is None:
                self.mplayer_process = subprocess.Popen(
                    ['mplayer.exe', '-slave', '-quiet', track.path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    close_fds=(sys.platform != 'win32')
                )
            else:
                load_command = ' '.join(['loadfile', track.path, '0', '\n'])
                try:
                    self.mplayer_process.stdin.write(load_command)
                except (TypeError, UnicodeEncodeError):
                    self.mplayer_process.stdin.write(load_command.encode('utf-8', 'ignore'))
                self.mplayer_process.stdin.flush()

    def pause(self):
        """ A method that pauses the player """
        if self.info.state == PlayerStateEnum.Playing:
            command = ' '.join(['pause', '\n'])
            try:
                self.mplayer_process.stdin.write(command)
            except (TypeError, UnicodeEncodeError):
                self.mplayer_process.stdin.write(command.encode('utf-8', 'ignore'))
            self.mplayer_process.stdin.flush()
            self.info.state = PlayerStateEnum.Paused

    def stop(self):
        """ A method that stops the player """
        if self.info.state == PlayerStateEnum.Playing or self.info.state == PlayerStateEnum.Paused:
            seek_command = ' '.join(['seek', '0', '2', '\n'])
            try:
                self.mplayer_process.stdin.write(seek_command)
            except (TypeError, UnicodeEncodeError):
                self.mplayer_process.stdin.write(seek_command.encode('utf-8', 'ignore'))
            self.mplayer_process.stdin.flush()
            pause_command = ' '.join(['pause', '\n'])
            try:
                self.mplayer_process.stdin.write(pause_command)
            except (TypeError, UnicodeEncodeError):
                self.mplayer_process.stdin.write(pause_command.encode('utf-8', 'ignore'))
            self.mplayer_process.stdin.flush()
            self.info.state = PlayerStateEnum.Stoped

    def volume(self, value):
        """ A method that sets the volume of the player """
        if value:
            volume_command = ' '.join(['volume', str(value), '1', '\n'])
            try:
                self.mplayer_process.stdin.write(volume_command)
            except (TypeError, UnicodeEncodeError):
                self.mplayer_process.stdin.write(volume_command.encode('utf-8', 'ignore'))
            self.mplayer_process.stdin.flush()
            self.info.volume = value

    def has_entries(self):
        """ A method that returns a boolean specifying whether there are entries on the playlist """
        playlist = pl.select_active()
        return playlist and isinstance(playlist, collections.Sequence)


class Player():
    """ Class that implements a basic music player """

    def __init__(self):
        self.info = PlayerInfo()
        if not pg.mixer.get_init():
            pg.mixer.pre_init()
            pg.mixer.init()

    def add(self, entry):
        """ Adds a new entry on the playlist """
        if entry is not None:
            playlist = pl.Playlist(entry)
            playlist.active = True
            pl.insert(playlist)

    def remove(self, id):
        """ A method that removes an entry from the playlist based on the provided id """
        if id is not None:
            playlist = pl.select_by_id(id)
            playlist.active = False
            pl.delete_by_id(id)

    def remove_all(self):
        """ A method that removes all entries from the playlist """
        pl.delete_all()

    def play(self, track=None):
        """ A method that plays music based on the state of the player """
        if (
                (
                    self.info.state == PlayerStateEnum.Paused or
                    self.info.state == PlayerStateEnum.Stoped
                ) and
                track is None
        ):
            pg.mixer.music.unpause()
            self.info.state = PlayerStateEnum.Playing

        elif self.info.state == PlayerStateEnum.Init and track is None:
            playlist = pl.select_active()
            if playlist:
                track = playlist.pop(0)
                pg.mixer.music.load(track.path)
                self.info.track = track
                self.info.state = PlayerStateEnum.Playing
                pg.mixer.music.play()

        elif track is not None:
            pg.mixer.music.load(track.path)
            self.info.track = track
            self.info.state = PlayerStateEnum.Playing
            pg.mixer.music.play()

    def play_all(self):
        """ A method that queues all the available songs of the playlist and then start playing """
        # Stop the player
        self.stop()
        self.info.state = PlayerStateEnum.Stoped
        # Get all the active tracks
        playlist = pl.select_active()
        # Checks if any track exists
        if playlist and isinstance(playlist, collections.Sequence):
            # Load the first track and queue the rest
            self.info.track = playlist.pop(0)
            pg.mixer.music.load(self.info.track.path)
            for entry in playlist:
                pg.mixer.music.queue(entry.path)
        # Call the play function and set the state to playing
        pg.mixer.music.play()
        self.info.state = PlayerStateEnum.Playing

    def pause(self):
        """ A method that pauses the player """
        if self.info.state == PlayerStateEnum.Playing:
            pg.mixer.music.pause()
            self.info.state = PlayerStateEnum.Paused

    def stop(self):
        """ A method that stops the player """
        if self.info.state == PlayerStateEnum.Playing or self.info.state == PlayerStateEnum.Paused:
            pg.mixer.music.rewind()
            self.pause()
            self.info.state = PlayerStateEnum.Stoped

    def next(self):
        """ A method that plays the next track on the playlist """
        pass

    def previous(self):
        """ A method that plays the previous track on the playlist """
        pass

    def volume(self, value):
        """ A method that sets the volume of the player """
        if value:
            pg.mixer.music.set_volume(value / 100)
            self.info.volume = value

    def has_entries(self):
        """ A method that returns a boolean specifying whether there are entries on the playlist """
        playlist = pl.select_active()
        return playlist and isinstance(playlist, collections.Sequence)


def emit_player_info():
    """ A function that sends the entry that is currently playing """
    info = dict(PLAYER.info)
    emit('player info', info, broadcast=True)


def emit_queue():
    """ A functions that sends the currently active tracks """
    emit('queue', [dict(entry) for entry in pl.select_active()])


@SOCKET_IO.on('player info', namespace='/server')
def player_info(_):
    """ A function that sends thew info of the player """
    emit_player_info()


@SOCKET_IO.on('play', namespace='/server')
def play_audio(_):
    """ A function that starts playing the first track on the playlist """
    PLAYER.play()
    emit_player_info()


@SOCKET_IO.on('play now', namespace='/server')
def play_now(data):
    """ A function that plays the track that is provided removing
        every source queued up until now
    """
    entries = pl.select_active_by_path(data['path'])
    if isinstance(entries, collections.Sequence) and entries:
        track = entries[0]
        PLAYER.play(track)
        emit_player_info()


@SOCKET_IO.on('play all', namespace='/server')
def play_all(_):
    """ A function that plays all the active entries in the playlist table """
    playlist = pl.select_active()
    if isinstance(playlist, collections.Sequence) and playlist:
        # start playing and emit the current track
        PLAYER.play_all()
        emit_player_info()


@SOCKET_IO.on('pause', namespace='/server')
def pause_audio(_):
    """ event handler for pausing the audio player """
    PLAYER.pause()
    emit_player_info()


@SOCKET_IO.on('stop', namespace='/server')
def stop_audio(_):
    """ event handler for stoping the audio player """
    PLAYER.stop()
    emit_player_info()


@SOCKET_IO.on('next', namespace='/server')
def next_track(_):
    """ starts playing the next track in the queue """
    PLAYER.next()
    emit_player_info()


@SOCKET_IO.on('volume', namespace='/server')
def volume_audio(data):
    """ event handler for controlling the volume of the audio player """
    PLAYER.volume(data)
    emit_player_info()


@SOCKET_IO.on('queue push', namespace='/server')
def queue_push(data):
    """ event handler for pushing a new track on the queue """
    PLAYER.add(data)
    emit_player_info()
    emit_queue()


@SOCKET_IO.on('queue pop', namespace='/server')
def queue_pop(data):
    """ event handler for poping a track from queue """
    PLAYER.remove(data)
    emit_queue()


@SOCKET_IO.on('queue', namespace='/server')
def queue(_):
    """ List queued tracks event handler """
    emit_player_info()
    emit_queue()


# audio player initialization and configuration
PLAYER = Player()
