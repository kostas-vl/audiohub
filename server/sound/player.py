"""
Contains event handlers for manipulating the player
"""
import sys
import datetime
import collections
import enum
import pafy
import models.playlist as pl
import models.streams as strm
import configuration.application_settings as app_settings
from flask_socketio import emit
from enviroment import SOCKET_IO
from backends.process_initiator import process_wrapper_init


class PlayerStateEnum(enum.Enum):
    """
    Enum that shows various player state values
    """
    Init = 'init'
    Stoped = 'stoped'
    Paused = 'paused'
    Playing = 'playing'


class PlayerInfo():
    """
    Class that holds information about a music player
    """

    def __init__(self):
        self.track = ''
        self.volume = 100
        self.state = PlayerStateEnum.Init
        self.time = 0
        self.time_str = '0:00'
        self.current_time = 0
        self.current_time_str = '0:00'

    def __iter__(self):
        yield 'track', dict(self.track)
        yield 'volume', self.volume
        yield 'state', self.state.value
        yield 'time', self.time
        yield 'timeStr', self.time_str
        yield 'currentTime', self.current_time
        yield 'currentTimeStr', self.current_time_str


class Player():
    """
    Class that interops with the mplayer
    """

    def __init__(self):
        self.info = PlayerInfo()
        self.backend_process = None
        self.streams_cache = []

    def init(self):
        """
        Sets when called specific attrs of the class\
        """
        self.backend_process = process_wrapper_init(
            app_settings.INSTANCE.backend
        )

    def add(self, entry):
        """
        Adds a new entry on the playlist
        """
        if entry is not None:
            playlist = pl.Playlist(entry)
            playlist.active = True
            pl.insert(playlist)

    def remove(self, playlist_id):
        """
        A method that removes an entry from the playlist based on the provided id
        """
        if playlist_id:
            pl.delete_by_id(playlist_id)

    def remove_all(self):
        """
        A method that removes all entries from the playlist
        """
        pl.delete_all()

    def play(self, data=None):
        """
        A method that plays music based on the state of the player
        """
        is_playing = not (
            self.info.state == PlayerStateEnum.Paused or self.info.state == PlayerStateEnum.Stoped
        )
        # Unpausing the player
        if not is_playing and data is None:
            self.backend_process.pause()
            self.info.state = PlayerStateEnum.Playing
        # Loading a single track
        elif data and isinstance(data, pl.Playlist):
            # Settings the track and state info
            self.info.track = data
            self.info.state = PlayerStateEnum.Playing
            # Loading the file
            self.backend_process.loadfile(self.info.track.path)
            # Experimental code for the linux platform
            if not is_playing and sys.platform == 'linux':
                self.backend_process.pause()
            # Setting the volume
            self.volume(self.info.volume)
            # Setting the total time info
            # self.info.time = self.backend_process.time()
            # self.info.time_str = convert_seconds_to_time_str(self.info.time)
        # Loading a list of tracks
        elif data and isinstance(data, collections.Sequence):
            # Settings the state info
            self.info.state = PlayerStateEnum.Playing
            # Stoping the playback
            self.backend_process.stop()
            # Loading all the files
            for entry in data:
                self.backend_process.loadfile(entry.path, True)
            # Setting the track info
            self.info.track = pl.Playlist(
                identity=-1,
                name='All Playlist...',
                type='file',
                active=True,
                date_created=datetime.datetime.now(),
                date_modified=datetime.datetime.now()
            )
            # Experimental code for the linux platform
            if not is_playing and sys.platform == 'linux':
                self.backend_process.pause()
            # Setting the volume
            self.volume(self.info.volume)

    def pause(self):
        """
        A method that pauses the player
        """
        if self.info.state == PlayerStateEnum.Playing:
            self.backend_process.pause()
            self.info.state = PlayerStateEnum.Paused

    def stop(self):
        """
        A method that stops the player
        """
        if self.info.state == PlayerStateEnum.Playing or self.info.state == PlayerStateEnum.Paused:
            self.backend_process.seek(0)
            self.backend_process.pause()
            self.info.state = PlayerStateEnum.Stoped

    def volume(self, value):
        """
        A method that sets the volume of the player
        """
        if value:
            self.backend_process.volume(value)
            if self.info.state == PlayerStateEnum.Stoped:
                self.info.state = PlayerStateEnum.Playing
                self.stop()
            elif self.info.state == PlayerStateEnum.Paused:
                self.info.state = PlayerStateEnum.Playing
                self.pause()
            self.info.volume = value

    def next(self):
        """
        A methods that moves to the next track on the queue
        """
        if self.info.track.identity == -1:
            if self.info.state != PlayerStateEnum.Playing:
                self.info.state = PlayerStateEnum.Playing
                # experimental code for linux
                if sys.platform == 'linux':
                    self.backend_process.pause()
            self.backend_process.next()

    def previous(self):
        """
        A method that moves to the previous track on the queue
        """
        if self.info.track.identity == -1:
            if self.info.state != PlayerStateEnum.Playing:
                self.info.state = PlayerStateEnum.Playing
                # experimental code for linux
                if sys.platform == 'linux':
                    self.backend_process.pause()
            self.backend_process.previous()

    def current_time(self):
        """
        A method that returns the current time position of the playback on the player
        """
        is_playing = self.info.state == PlayerStateEnum.Playing
        track_ended = self.info.current_time >= self.info.time - 1
        if is_playing and not track_ended:
            current_time = self.backend_process.current_time()
            if current_time is None:
                self.stop()
            else:
                self.info.current_time = current_time
            self.info.current_time_str = convert_seconds_to_time_str(
                self.info.current_time
            )
        return (self.info.current_time, self.info.current_time_str)

    def has_entries(self):
        """
        A method that returns a boolean specifying whether there are entries on the playlist
        """
        playlist = pl.select_active()
        return playlist and isinstance(playlist, collections.Sequence)

    def load_stream(self, url):
        """
        Loads a stream to mplayer
        """
        # Checking if a url is given
        if url:
            stream = None
            streams = strm.select_by_url(url)
            # Check if there are streams in the database with the same url and in cache
            if streams and streams[0].identity in self.streams_cache:
                stream = streams[0]
            else:
                # Add the track in memory
                video = pafy.new(url)
                best_audio = video.getbestaudio(preftype="webm")
                # Insert or update to the database the stream information
                if streams:
                    streams[0].player_url = best_audio.url
                    stream = strm.update(streams[0])
                else:
                    stream = strm.Stream(
                        title=video.title,
                        url=url,
                        player_url=best_audio.url
                    )
                    strm.insert(stream)
                # Add it to the player stream cache
                self.streams_cache.append(stream.identity)
            # Load the file and start the playback
            self.backend_process.loadfile(stream.player_url)
            self.backend_process.volume(self.info.volume)
            self.info.track = pl.Playlist(
                identity=-1,
                name='(Streaming) ' + stream.title,
                type='file',
                active=True,
                date_created=datetime.datetime.now(),
                date_modified=datetime.datetime.now()
            )
            self.info.state = PlayerStateEnum.Playing
            # Setting the total time info
            # self.info.time = self.backend_process.time()
            # self.info.time_str = convert_seconds_to_time_str(self.info.time)


def convert_seconds_to_time_str(value):
    """
    Converts the given seconds to a time string of format m:ss
    """
    # Getting its float value
    time_float = float(value)
    # Getting the minutes and seconds
    minutes, seconds = divmod(time_float, 60)
    # Creating the time values in a string format
    return str(int(minutes)) + ':' + str(int(seconds))


def emit_player_info():
    """
    A function that sends the entry that is currently playing
    """
    info = dict(INSTANCE.info)
    emit('player info', info, broadcast=True)


def emit_queue():
    """
    A functions that sends the currently active tracks
    """
    try:
        emit('queue', [dict(entry) for entry in pl.select_active()])
    except Exception as err:
        print(err)
        raise err


def emit_stream_history():
    """
    A function that sends all registered streams
    """
    try:
        emit('stream history', [dict(entry) for entry in strm.select()])
    except Exception as err:
        print(err)
        raise err


@SOCKET_IO.on('player info', namespace='/server')
def on_player_info(_):
    """
    A function that sends thew info of the player
    """
    emit_player_info()


@SOCKET_IO.on('play', namespace='/server')
def on_play(data):
    """
    A function that plays the track that is provided removing
    every source queued up until now
    """
    if data:
        entries = pl.select_active_by_path(data['path'])
        if isinstance(entries, collections.Sequence) and entries:
            track = entries[0]
            INSTANCE.play(track)
            emit_player_info()
    else:
        INSTANCE.play()
        emit_player_info()


@SOCKET_IO.on('play all', namespace='/server')
def on_play_all(_):
    """
    A function that plays all the active entries in the playlist table
    """
    playlist = pl.select_active()
    if isinstance(playlist, collections.Sequence) and playlist:
        # start playing and emit the current track
        INSTANCE.play(playlist)
        emit_player_info()


@SOCKET_IO.on('pause', namespace='/server')
def on_pause(_):
    """
    Event handler for pausing the audio player
    """
    INSTANCE.pause()
    emit_player_info()


@SOCKET_IO.on('stop', namespace='/server')
def on_stop(_):
    """
    Event handler for stoping the audio player
    """
    INSTANCE.stop()
    emit_player_info()


@SOCKET_IO.on('previous', namespace='/server')
def on_previous(_):
    """
    Starts playing the previous track in the queue
    """
    INSTANCE.previous()
    emit_player_info()


@SOCKET_IO.on('next', namespace='/server')
def on_next(_):
    """
    Starts playing the next track in the queue
    """
    INSTANCE.next()
    emit_player_info()


@SOCKET_IO.on('volume', namespace='/server')
def on_volume(data):
    """
    Event handler for controlling the volume of the audio player
    """
    INSTANCE.volume(data)
    emit_player_info()


@SOCKET_IO.on('current time', namespace='/server')
def on_current_time(_):
    """
    Event handler for fetching the current time on the audio player
    """
    time, time_str = INSTANCE.current_time()
    emit('current time', {'currentTime': time, 'currentTimeStr': time_str})


@SOCKET_IO.on('queue push', namespace='/server')
def on_queue_push(data):
    """
    Event handler for pushing a new track on the queue
    """
    INSTANCE.add(data)
    emit_player_info()
    emit_queue()


@SOCKET_IO.on('queue pop', namespace='/server')
def on_queue_pop(data):
    """
    Event handler for poping a track from queue
    """
    INSTANCE.remove(data)
    emit_queue()


@SOCKET_IO.on('queue', namespace='/server')
def on_queue(_):
    """
    List queued tracks event handler
    """
    emit_player_info()
    emit_queue()


@SOCKET_IO.on('stream history', namespace='/server')
def on_stream_history(_):
    """
    List all registered streams
    """
    emit_stream_history()


@SOCKET_IO.on('load stream', namespace='/server')
def on_load_stream(url):
    """
    Load an incoming stream to mplayer
    """
    if url:
        INSTANCE.load_stream(url)
        emit_player_info()
        emit('load stream complete')
        emit_stream_history()


# audio player initialization and configuration
INSTANCE = Player()
