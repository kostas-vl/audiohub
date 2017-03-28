import pyglet
from flask_socketio import emit
from enviroment import *
from sound.playlist import *
from drive.file_system import *

# Audio player initialization and configuration
audioPlayer = pyglet.media.Player()

playlist_collection = []

# Starts playing the first track on the playlist
@socketio.on('play', namespace='/server')
def play_audio(data):
    if not audioPlayer.playing:
        source = pyglet.media.load(playlist_collection[0].path)
        audioPlayer.queue(source)
        audioPlayer.play()


# Play track that is provided event handler
@socketio.on('play now', namespace='/server')
def play_now(file): 
    audioPlayer.next_source()
    entries = [entry for entry in playlist_collection if entry.path == file['path']]
    if len(entries) > 0:
        source = pyglet.media.load(entries[0].path)
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
    playlist_collection.append(Playlist(entry))
    queue(None)


# Pop track from queue event handler
@socketio.on('queue pop', namespace='/server')
def queue_pop(path):
    playlist_collection = filter(lambda x: x.path != path, playlist_collection)
    queue(None)


# List queued tracks event handler
@socketio.on('queue', namespace='/server')
def queue(data):
    emit('queue', [dict(entry) for entry in playlist_collection])
