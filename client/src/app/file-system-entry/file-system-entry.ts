export class FileSystemEntry {

    public name: string;
    public type: 'file' | 'directory';
    public path: string;
    public entries: FileSystemEntry[];

    constructor(name: string, type: 'file' | 'directory', path: string) {
        this.name = name;
        this.type = type;
        this.path = path;
    }

}
