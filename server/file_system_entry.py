class FileSystemEntry():
    Name = ''
    Type = ''
    Path = ''

    def __init__(self, name, type, path):
        self.Name = name
        self.Type = type
        self.Path = path

    def __iter__(self):
        yield 'name', self.Name
        yield 'type', self.Type
        yield 'path', self.Path