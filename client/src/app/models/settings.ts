import { SoundDirection } from './sound-direction';

export interface ISettings {

    identity: number;
    user_id: number;
    dark_theme: boolean;
    sidenav_mode: 'over' | 'side' | 'push';
    sound_direction: 'server' | 'user';
    date_created: Date |string;
    date_modified: Date | string;

}

export class Settings implements ISettings {

    public identity = 0;
    public user_id = 0;
    public dark_theme = true;
    public sidenav_mode: 'over' | 'side' | 'push' = 'side';
    public sound_direction: 'server' | 'user' = 'server';
    public date_created: Date | string = '';
    public date_modified: Date | string = '';

}
