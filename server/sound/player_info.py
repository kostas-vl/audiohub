"""
Module that exposes the player info class.
"""
from sound.player_state import PlayerStateEnum


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
