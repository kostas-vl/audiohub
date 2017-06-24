export interface IPlaylist {

    identity: number;
    name: string;
    type: 'file' | 'directory';
    path: string;
    active: number;
    date_created: Date | string;
    date_modified: Date | string;

}

export class Playlist implements IPlaylist {

    public identity = 0;
    public name = '';
    public type: 'file' | 'directory' = 'file';
    public path = '';
    public active = 0;
    public date_created: Date | string = '';
    public date_modified: Date | string = '';

}
