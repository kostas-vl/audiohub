export interface IDownloadDetails {

    system: string;
    url: string;
    fileFormat: 'mp3' | 'mp4' | 'wav';

}

export class DownloadDetails implements IDownloadDetails {

    public system = '';
    public url = '';
    public fileFormat: 'mp3' | 'mp4' | 'wav' = 'wav';

}
