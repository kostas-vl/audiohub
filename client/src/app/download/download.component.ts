import { Component, OnInit } from '@angular/core';
import { IDownloadDetails, DownloadDetails } from '../models/download-details';
import { SocketService } from '../socket/socket.service';
import { PageLoaderService } from '../page-loader-service/page-loader.service';

@Component({
    selector: 'app-download',
    templateUrl: './download.component.html',
    styleUrls: ['./download.component.scss']
})
export class DownloadComponent implements OnInit {

    public details: IDownloadDetails = new DownloadDetails();
    public formatOptions = [
        'mp3',
        'mp4',
        'wav'
    ];

    /**
     * Creates an instance of DownloadComponent.
     * @memberof DownloadComponent
     */
    constructor(
        private pageLoader: PageLoaderService,
        private socket: SocketService
    ) { }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof DownloadComponent
     */
    public ngOnInit() { }

    /**
     * Requests a download from the server
     * @param {IDownloadDetails} details of the download
     * @memberof DownloadComponent
     */
    public onDownload(details: IDownloadDetails) {
        if (details) {
            this.pageLoader.start();
            this.socket.emit('download', details);
            this.details = new DownloadDetails();
        }
    }

}
