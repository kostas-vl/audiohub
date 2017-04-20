import pyglet
import sound.playlist as pl
from flask_socketio import emit
from enviroment import *
from drive.file_system import *

# audio player initialization and configuration
audio_player = pyglet.media.Player()


def currently_playling(entry):  # sends the entry that is currently playing
    emit('currently playing', dict(entry))


def emit_queue():  # sends the currently active tracks
    emit('queue', [dict(entry) for entry in pl.select_active()])


@socketio.on('play', namespace='/server')
def play_audio(data):  # starts playing the first track on the playlist
    if not audio_player.playing:
        playlist_collection = pl.select_active()
        source = pyglet.media.load(playlist_collection[0].path)
        audio_player.queue(source)
        audio_player.play()
        currently_playling(playlist_collection[0])


@socketio.on('play now', namespace='/server')
def play_now(data):  # play track that is provided event handler
    # removing every source queued up until now
    while audio_player.source is not None:
        audio_player.next_source()

    # getting all the active entries with the provided path
    entries = pl.select_active_by_path(data['path'])

    # if there are entries, the first entry is queued and the the audio player
    # start playing
    if len(entries) > 0:
        source = pyglet.media.load(entries[0].path)
        audio_player.queue(source)
        audio_player.play()
        currently_playling(entries[0])


@socketio.on('play all', namespace='/server')
def play_all(data):  # play all the active entries in the playlist table
    # pauses the audio player
    if audio_player.playing:
        audio_player.pause()

    # removes all the source currently queued
    while audio_player.source is not None:
        audio_player.next_source()

    # gets all the active entries in the playlsit table
    playlist = pl.select_active()
    if len(playlist) > 0:
        # queue all the entries available
        for track in playlist:
            source = pyglet.media.load(track.path)
            audio_player.queue(source)

        # start playing and emit the current track
        audio_player.play()
        currently_playling(playlist[0])


@socketio.on('pause', namespace='/server')
def pause_audio(data):  # event handler for pausing the audio player
    audio_player.pause()


@socketio.on('stop', namespace='/server')
def stop_audio(data):  # event handler for stoping the audio player
    audio_player.pause()
    audio_player.seek(0)


@socketio('next', namespace='/server')
def next_track(data):  # starts playing the next track in the queue
    audio_player.next_source()


@socketio.on('volume', namespace='/server')
def volume_audio(data):  # event handler for controlling the volume of the audio player
    audio_player.volume = data / 100


@socketio.on('queue push', namespace='/server')
def queue_push(entry):  # event handler for pushing a new track on the queue
    playlist = pl.Playlist(entry)
    playlist.active = True
    pl.insert(playlist)
    emit_queue()


@socketio.on('queue pop', namespace='/server')
def queue_pop(data):  # event handler for poping a track from queue
    playlist = pl.select_by_id(data)
    playlist.active = False
    pl.update_by_id(playlist)
    emit_queue()


@socketio.on('queue', namespace='/server')
def queue(data):  # List queued tracks event handler
    emit_queue()
