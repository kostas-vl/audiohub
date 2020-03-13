"""
Contains event handlers for manipulating the player
"""
import sys
import datetime
import collections
import pafy
import models.playlist as pl
import models.streams as strm
from configuration import APP_SETTINGS_INSTANCE
from sound.player_info import PlayerInfo
from sound.player_state import PlayerStateEnum
from backends import create_backend
from flask_socketio import emit


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
        Sets when called specific attrs of the class.
        """
        self.backend_process = create_backend(APP_SETTINGS_INSTANCE.backend)

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
        A method that removes an entry from the playlist based
        on the provided id.
        """
        if playlist_id:
            pl.delete_by_id(playlist_id)

    def remove_all(self):
        """
        A method that removes all entries from the playlist.
        """
        pl.delete_all()

    def play(self, data=None):
        """
        A method that plays music based on the state of the player
        """
        is_playing = not (
            self.info.state == PlayerStateEnum.Paused
            or self.info.state == PlayerStateEnum.Stoped
        )
        if not is_playing and data is None:
            # Unpausing the player
            self.backend_process.pause()
            self.info.state = PlayerStateEnum.Playing
        elif data and isinstance(data, pl.Playlist):
            # Setting and loading a signle track and changing
            # the player's state. Also set the volume and the
            # time information.
            self.info.track = data
            self.info.state = PlayerStateEnum.Playing
            self.backend_process.loadfile(self.info.track.path)
            # Experimental code for the linux platform
            if not is_playing and sys.platform == 'linux':
                self.backend_process.pause()
            self.volume(self.info.volume)
            try:
                self.info.time = self.backend_process.time()
                self.info.time_str = convert_seconds_to_time_str(
                    self.info.time
                )
            except:
                self.info.time = 0
                self.info.time_str = '0:00'
        elif data and isinstance(data, collections.Sequence):
            # Setting and loading a list of tracks and changing
            # the player's state. Also set the volume.
            self.info.state = PlayerStateEnum.Playing
            self.backend_process.stop()
            for entry in data:
                self.backend_process.loadfile(entry.path, True)
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
        can_stop = (
            self.info.state == PlayerStateEnum.Playing
            or self.info.state == PlayerStateEnum.Paused
        )
        if can_stop:
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
        A method that returns the current time position of the playback
        on the player
        """
        is_playing = self.info.state == PlayerStateEnum.Playing
        track_ended = self.info.current_time >= self.info.time - 1
        if is_playing and not track_ended:
            try:
                current_time = self.backend_process.current_time()
            except:
                current_time = 0
            if not current_time:
                self.stop()
            else:
                self.info.current_time = current_time
            self.info.current_time_str = convert_seconds_to_time_str(
                self.info.current_time
            )
        return (self.info.current_time, self.info.current_time_str)

    def has_entries(self):
        """
        A method that returns a boolean specifying whether there are entries
        on the playlist
        """
        playlist = pl.select_active()
        return playlist and isinstance(playlist, collections.Sequence)

    def load_stream(self, url):
        """
        Loads a stream to mplayer
        """
        if url:
            stream = None
            streams = strm.select_by_url(url)
            if streams and streams[0].identity in self.streams_cache:
                stream = streams[0]
            else:
                video = pafy.new(url)
                best_audio = video.getbestaudio(preftype="webm")
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
                self.streams_cache.append(stream.identity)
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
    minutes, seconds = divmod(value, 60)
    return str(int(minutes)) + ':' + str(int(seconds))


PLAYER_INSTANCE = Player()
