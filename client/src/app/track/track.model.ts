export enum TrackType {
    Unknown = 0,
    File = 1,
    NasFile = 2,
    Youtube = 3
}

export interface ITrack {
    name: string;
    type: TrackType;
    url: string;
}

export class Track implements ITrack {
    public name: string;
    public type: TrackType;
    public url: string;

    constructor(name: string, type: TrackType, url: string) {
        this.name = name;
        this.type = type;
        this.url = url;
    }
}
