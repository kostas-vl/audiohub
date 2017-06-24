export interface IFileSystem {

    identity: number;
    name: string;
    type: 'file' | 'directory';
    path: string;
    active: number;
    dateCreated: Date | string;
    dateModified: Date | string;

}

export class FileSystem implements IFileSystem {

    public identity: number;
    public name: string;
    public type: 'file' | 'directory';
    public path: string;
    public active: number;
    public dateCreated: Date | string;
    public dateModified: Date | string;

}
