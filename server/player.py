import pyglet
from flask_socketio import emit
from enviroment import *
from track import *

# Audio player initialization and configuration
# finalFantasyTheme = Track('Final Fantasy Main Theme',
#                           TrackType.File, 'C:/Users/kvl_9/Music/fantasy.mp3')
# audioSource = pyglet.media.load(finalFantasyTheme.Url)
audioPlayer = pyglet.media.Player()
# audioPlayer.queue(audioSource)

# Playlist initialization
playlist = []


# Play event handler
@socketio.on('play', namespace='/server')
def play_audio(data):
    if not audioPlayer.playing:
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


# Push neew track on queue event handler
@socketio.on('queue push', namespace='/server')
def queue_push(data):
    if data.type == TrackType.File:
        track = Track(data.name, data.type, data.url)
        audioPlayer.queue(data.Url)
        playlist.append(track)

    elif data.type == TrackType.NetworkFile:
        track = Track(data.name, data.type, data.url)
        audioPlayer.queue(data.url)
        playlist.append(track)
        pass

    elif data.type == TrackType.YoutubeStream:
        pass

    else:
        pass

    queue()


# List queued tracks event handler
@socketio.on('queue', namespace='/server')
def queue(data):
    json_playlist = list(map(lambda x: x.Json(), playlist))
    emit('queue', json_playlist)
