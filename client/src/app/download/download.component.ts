import { Component, OnInit } from '@angular/core';
import { IDownloadDetails, DownloadDetails } from '../models/download-details';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-download',
    templateUrl: './download.component.html',
    styleUrls: ['./download.component.css']
})
export class DownloadComponent implements OnInit {

    public details: IDownloadDetails = new DownloadDetails();
    public formatOptions = [
        'mp3',
        'mp4',
        'wav'
    ];

    constructor(private socket: SocketService) { }

    ngOnInit() { }

    public onDownload(details: IDownloadDetails) {
        if (details) {
            this.socket.emit('download', details);
            this.details = new DownloadDetails();
        }
    }

}
