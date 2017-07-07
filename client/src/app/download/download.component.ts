import { Component, OnInit } from '@angular/core';
import { IDownloadDetails, DownloadDetails } from '../models/download-details';
import { SocketService } from '../socket/socket.service';
import { PageLoaderService } from '../page-loader-service/page-loader.service';

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

    constructor(
        private pageLoader: PageLoaderService,
        private socket: SocketService
    ) { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() { }

    /**
     * requests a download from the server
     * @param {IDownloadDetails} details of the download
     */
    public onDownload(details: IDownloadDetails) {
        if (details) {
            this.pageLoader.start();
            this.socket.emit('download', details);
            this.details = new DownloadDetails();
        }
    }

}
