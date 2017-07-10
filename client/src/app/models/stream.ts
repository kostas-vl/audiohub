export interface IStream {

    identity: string;
    title: string;
    url: string;
    player_url: string;
    date_created: Date | string;

}

export class Stream implements IStream {

    public identity = '';
    public title = '';
    public url = '';
    public player_url = '';
    public date_created = '';

}
