class FileSystemEntry():
    Id = None
    Name = None
    Type = None
    Path = None
    Date_Created = None
    Active = None

    def __init__(self, name, type, path):
        self.Name = name
        self.Type = type
        self.Path = path

    def __iter__(self):
        yield 'id', self.Id
        yield 'name', self.Name
        yield 'type', self.Type
        yield 'path', self.Path
        yield 'dateCreated', self.Date_Created