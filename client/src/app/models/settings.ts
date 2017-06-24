import { SoundDirection } from './sound-direction';

export interface ISettings {

    darkTheme: boolean;
    sidenavMode: 'over' | 'side' | 'push';
    soundDirection: SoundDirection;

}

export class Settings implements ISettings {

    public darkTheme = true;
    public sidenavMode: 'over' | 'side' | 'push' = 'side';
    public soundDirection: SoundDirection = SoundDirection.Server;

}
