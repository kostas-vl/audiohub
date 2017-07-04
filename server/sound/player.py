""" Contains event handlers for manipulating the player """
import sys
import collections
import enum
import pafy
import models.playlist as pl
import sound.mplayer as mpl
from flask_socketio import emit
from enviroment import APP, SOCKET_IO


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


class Player():
    """ Class that interops with the mplayer """

    def __init__(self):
        self.info = PlayerInfo()
        self.mplayer_process = mpl.MplayerProcess()

    def init(self):
        """ Initializes at a specified time the mplayer process """
        self.mplayer_process = mpl.MplayerProcess()

    def add(self, entry):
        """ Adds a new entry on the playlist """
        if entry is not None:
            playlist = pl.Playlist(entry)
            playlist.active = True
            pl.insert(playlist)

    def remove(self, id):
        """ A method that removes an entry from the playlist based on the provided id """
        if id:
            pl.delete_by_id(id)

    def remove_all(self):
        """ A method that removes all entries from the playlist """
        pl.delete_all()

    def play(self, data=None):
        """ A method that plays music based on the state of the player """
        is_playing = not (
            self.info.state == PlayerStateEnum.Paused or self.info.state == PlayerStateEnum.Stoped
        )
        # Unpausing the player
        if not is_playing and data is None:
            self.mplayer_process.pause()
            self.info.state = PlayerStateEnum.Playing
        # Loading a single track
        elif data and isinstance(data, pl.Playlist):
            self.info.track = data
            self.info.state = PlayerStateEnum.Playing
            self.mplayer_process.loadfile(self.info.track.path)
            # experimental code for the linux platform
            if not is_playing and sys.platform == 'linux':
                self.mplayer_process.pause()
            self.volume(self.info.volume)
        # Loading a list of tracks
        elif data and isinstance(data, collections.Sequence):
            self.info.state = PlayerStateEnum.Playing
            self.mplayer_process.stop()
            for entry in data:
                self.mplayer_process.loadfile(entry.path, True)
            self.info.track = pl.Playlist(
                identity=-1,
                name='All Playlist...',
                type='file',
                active=True,
                date_created=None,
                date_modified=None
            )
            # experimental code for the linux platform
            if not is_playing and sys.platform == 'linux':
                self.mplayer_process.pause()
            self.volume(self.info.volume)

    def pause(self):
        """ A method that pauses the player """
        if self.info.state == PlayerStateEnum.Playing:
            self.mplayer_process.pause()
            self.info.state = PlayerStateEnum.Paused

    def stop(self):
        """ A method that stops the player """
        if self.info.state == PlayerStateEnum.Playing or self.info.state == PlayerStateEnum.Paused:
            self.mplayer_process.seek(0, 2)
            self.mplayer_process.pause()
            self.info.state = PlayerStateEnum.Stoped

    def volume(self, value):
        """ A method that sets the volume of the player """
        if value:
            self.mplayer_process.volume(value)
            self.info.volume = value

    def next(self):
        """ A methods that moves to the next track on the queue """
        if self.info.track.identity == -1:
            if self.info.state != PlayerStateEnum.Playing:
                self.info.state = PlayerStateEnum.Playing
                # experimental code for linux
                if sys.platform == 'linux':
                    self.mplayer_process.pause()
            self.mplayer_process.next()

    def previous(self):
        """ A method that moves to the previous track on the queue """
        if self.info.track.identity == -1:
            if self.info.state != PlayerStateEnum.Playing:
                self.info.state = PlayerStateEnum.Playing
                # experimental code for linux
                if sys.platform == 'linux':
                    self.mplayer_process.pause()
            self.mplayer_process.previous()

    def has_entries(self):
        """ A method that returns a boolean specifying whether there are entries on the playlist """
        playlist = pl.select_active()
        return playlist and isinstance(playlist, collections.Sequence)

    def load_stream(self, url):
        """ Loads a stream to mplayer """
        stream = pafy.new(url)
        best_audio = stream.getbestaudio(preftype="webm")
        print(best_audio.url)


def emit_player_info():
    """ A function that sends the entry that is currently playing """
    info = dict(PLAYER.info)
    emit('player info', info, broadcast=True)


def emit_queue():
    """ A functions that sends the currently active tracks """
    try:
        emit('queue', [dict(entry) for entry in pl.select_active()])
    except Exception as err:
        print(err)
        raise err


@SOCKET_IO.on('player info', namespace='/server')
def on_player_info(_):
    """ A function that sends thew info of the player """
    emit_player_info()


@SOCKET_IO.on('play', namespace='/server')
def on_play(data):
    """ A function that plays the track that is provided removing
        every source queued up until now
    """
    if data:
        entries = pl.select_active_by_path(data['path'])
        if isinstance(entries, collections.Sequence) and entries:
            track = entries[0]
            PLAYER.play(track)
            emit_player_info()
    else:
        PLAYER.play()
        emit_player_info()


@SOCKET_IO.on('play all', namespace='/server')
def on_play_all(_):
    """ A function that plays all the active entries in the playlist table """
    playlist = pl.select_active()
    if isinstance(playlist, collections.Sequence) and playlist:
        # start playing and emit the current track
        PLAYER.play(playlist)
        emit_player_info()


@SOCKET_IO.on('pause', namespace='/server')
def on_pause(_):
    """ event handler for pausing the audio player """
    PLAYER.pause()
    emit_player_info()


@SOCKET_IO.on('stop', namespace='/server')
def on_stop(_):
    """ event handler for stoping the audio player """
    PLAYER.stop()
    emit_player_info()


@SOCKET_IO.on('previous', namespace='/server')
def on_previous(_):
    """ starts playing the previous track in the queue """
    PLAYER.previous()
    emit_player_info()


@SOCKET_IO.on('next', namespace='/server')
def on_next(_):
    """ starts playing the next track in the queue """
    PLAYER.next()
    emit_player_info()


@SOCKET_IO.on('volume', namespace='/server')
def on_volume(data):
    """ event handler for controlling the volume of the audio player """
    PLAYER.volume(data)
    emit_player_info()


@SOCKET_IO.on('queue push', namespace='/server')
def on_queue_push(data):
    """ event handler for pushing a new track on the queue """
    PLAYER.add(data)
    emit_player_info()
    emit_queue()


@SOCKET_IO.on('queue pop', namespace='/server')
def on_queue_pop(data):
    """ event handler for poping a track from queue """
    PLAYER.remove(data)
    emit_queue()


@SOCKET_IO.on('queue', namespace='/server')
def on_queue(_):
    """ List queued tracks event handler """
    emit_player_info()
    emit_queue()


@SOCKET_IO.on('load stream', namespace='/server')
def on_load_stream(data):
    """ Load an incoming stream to mplayer """
    try:
        if data:
            PLAYER.load_stream(data)
    except Exception as err:
        print(err)
        raise err


# audio player initialization and configuration
PLAYER = Player()
