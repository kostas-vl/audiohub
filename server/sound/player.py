import pyglet
from flask_socketio import emit
from enviroment import *
from drive.file_system_entry import *

# Audio player initialization and configuration
audioPlayer = pyglet.media.Player()

playlist = []

# Starts playing the first track on the playlist
@socketio.on('play', namespace='/server')
def play_audio(data):
    if not audioPlayer.playing:
        source = pyglet.media.load(playlist[0].Path)
        audioPlayer.queue(source)
        audioPlayer.play()


# Play track that is provided event handler
@socketio.on('play now', namespace='/server')
def play_now(file): 
    audioPlayer.next_source()
    entries = [entry for entry in playlist if entry.Path == file['path']]
    if len(entries) > 0:
        source = pyglet.media.load(entries[0].Path)
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
    entry = FileSystemEntry(entry['name'], entry['type'], entry['path'])
    playlist.append(entry)
    queue(None)


# Pop track from queue event handler
@socketio.on('queue pop', namespace='/server')
def queue_pop(path):
    playlist = filter(lambda x: x.path != path, playlist)
    queue(None)


# List queued tracks event handler
@socketio.on('queue', namespace='/server')
def queue(data):
    emit('queue', [dict(entry) for entry in playlist])
