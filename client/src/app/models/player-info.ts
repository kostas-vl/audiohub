import { IPlaylist, Playlist } from './playlist';

export interface IPlayerInfo {

    track: IPlaylist;
    volume: number;
    state: 'init' | 'stoped' | 'paused' | 'playing';

}

export class PlayerInfo implements IPlayerInfo {

    public track: IPlaylist = new Playlist();
    public volume = 100;
    public state: 'init' | 'stoped' | 'paused' | 'playing' = 'init';

}
