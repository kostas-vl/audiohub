import pyglet
import sound.playlist as pl
from flask_socketio import emit
from enviroment import *
from drive.file_system import *

# Audio player initialization and configuration
audioPlayer = pyglet.media.Player()


# Starts playing the first track on the playlist
@socketio.on('play', namespace='/server')
def play_audio(data):
    if not audioPlayer.playing:
        playlist_collection = pl.select_active()
        source = pyglet.media.load(playlist_collection[0].path)
        audioPlayer.queue(source)
        audioPlayer.play()


# Play track that is provided event handler
@socketio.on('play now', namespace='/server')
def play_now(file):
    audioPlayer.next_source()
    entries = [entry for entry in pl.select_active() if entry.path ==
               file['path']]
    if len(entries) > 0:
        source = pyglet.media.load(entries[0].path)
        audioPlayer.queue(source)
        audioPlayer.play()

@socketio.on('play all', namespace='/server')
def play_all(data):
    while audioPlayer.playing:
        audioPlayer.next_source()

    playlist = pl.select_active()
    for track in playlist:
        source = pyglet.media.load(track.path)
        audioPlayer.queue(source)

    audioPlayer.play()


# Pause event handler
@socketio.on('pause', namespace='/server')
def pause_audio(data):
    audioPlayer.pause()


# Stop event handler
@socketio.on('stop', namespace='/server')
def stop_audio(data):
    audioPlayer.pause()
    audioPlayer.seek(0)


# Volume event handler
@socketio.on('volume', namespace='/server')
def volume_audio(data):
    audioPlayer.volume = data / 100


# Push new track on queue event handler
@socketio.on('queue push', namespace='/server')
def queue_push(entry):
    playlist = pl.Playlist(entry)
    playlist.active = True
    pl.insert(playlist)
    emit_queue()


# Pop track from queue event handler
@socketio.on('queue pop', namespace='/server')
def queue_pop(data):
    playlist = pl.select_by_id(data)
    playlist.active = False
    pl.update_by_id(playlist)
    emit_queue()


# List queued tracks event handler
@socketio.on('queue', namespace='/server')
def queue(data):
    emit_queue()


def emit_queue():
    emit('queue', [dict(entry) for entry in pl.select_active()])
