import { Component, OnInit } from '@angular/core';
import { IStream } from '../models/stream';
import { SocketService } from '../socket/socket.service';
import { PageLoaderService } from '../page-loader-service/page-loader.service';

@Component({
    selector: 'app-stream',
    templateUrl: './stream.component.html',
    styleUrls: ['./stream.component.css']
})
export class StreamComponent implements OnInit {

    public url: string = null;
    public streamHistory: IStream[] = [];

    constructor(
        private pageLoader: PageLoaderService,
        private socket: SocketService
    ) { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() {
        // subscribes an event handler for the 'stream history' event
        this.socket.subscribe('stream history', (history: IStream[]) => {
            this.streamHistory = history;
        });

        // send an event message for the list of the stream history
        this.socket.emit('stream history');
    }

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

    /**
     * request a load registeres stream to the server
     */
    public onLoad(stream: IStream) {
        if (stream && stream.identity) {
            this.socket.emit('load registered stream', stream.identity);
        }
    }

    /**
     * request the stream history
     */
    public onRefresh() {
        this.socket.emit('stream history');
    }

}
