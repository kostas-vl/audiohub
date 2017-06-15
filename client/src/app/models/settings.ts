export interface ISettings {

    darkTheme: boolean;
    sidenavMode: 'over' | 'side' | 'push';

}

export class Settings implements ISettings {

    public darkTheme = true;
    public sidenavMode: 'over' | 'side' | 'push' = 'side';

}
