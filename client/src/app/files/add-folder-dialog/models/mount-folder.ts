export interface IMountFolder {

    ip: string;
    volume: string;
    user: string;
    password: string;

}

export class MountFolder implements IMountFolder {

    public ip = '';
    public volume = '';
    public user = '';
    public password = '';

}
