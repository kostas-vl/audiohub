import { Component, OnInit } from '@angular/core';
import { SocketService } from '../socket/socket.service';
import { PageLoaderService } from '../page-loader-service/page-loader.service';

@Component({
    selector: 'app-stream',
    templateUrl: './stream.component.html',
    styleUrls: ['./stream.component.css']
})
export class StreamComponent implements OnInit {

    public url: string = null;

    constructor(
        private pageLoader: PageLoaderService,
        private socket: SocketService
    ) { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() { }

    /**
     * request a load stream to the server
     * @param {string} url that is requested for playback
     */
    public onRequestStream(url: string) {
        if (url) {
            this.pageLoader.start();
            this.socket.emit('load stream', url);
            this.url = null;
        }
    }

}
