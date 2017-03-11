from enum import IntEnum


class TrackType(IntEnum):
    Unknown = 0
    File = 1
    NetworkFile = 2
    YoutubeStream = 3


class Track:
    Name = ''
    Type = TrackType.Unknown
    Url = ''

    def __init__(self, name, type, url):
        self.Name = name
        self.Type = type
        self.Url = url

    def Json(self):
        return {
            'name': self.Name,
            'type': self.Type,
            'url': self.Url
        }
