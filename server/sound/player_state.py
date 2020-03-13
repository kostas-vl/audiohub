"""
Module that exposes the player state enum.
"""
import enum


class PlayerStateEnum(enum.Enum):
    """
    Enum that shows various player state values
    """
    Init = 'init'
    Stoped = 'stoped'
    Paused = 'paused'
    Playing = 'playing'
