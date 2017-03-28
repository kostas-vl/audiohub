export interface IPlaylist {

    id: number;
    name: string;
    type: 'file' | 'directory';
    path: string;
    active: number;
    dateCreated: Date | string;
    dateModified: Date | string;

}

export class Playlist implements IPlaylist {

    public id: number;
    public name: string;
    public type: 'file' | 'directory';
    public path: string;
    public active: number;
    public dateCreated: Date | string;
    public dateModified: Date | string;

}
