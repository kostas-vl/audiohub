import { IPlaylist, Playlist } from './playlist';

export interface IPlayerInfo {

    track: IPlaylist;
    volume: number;
    state: 'init' | 'stoped' | 'paused' | 'playing';
    time: number;
    timeStr: string;
    currentTime: number;
    currentTimeStr: string;

}

export class PlayerInfo implements IPlayerInfo {

    public track: IPlaylist = new Playlist();
    public volume = 100;
    public state: 'init' | 'stoped' | 'paused' | 'playing' = 'init';
    public time = 0;
    public timeStr = '0:00';
    public currentTime = 0;
    public currentTimeStr = '0:00';

}
