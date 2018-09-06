import { Component, OnInit, OnDestroy } from '@angular/core';
import { IStream } from '../models/stream';
import { SocketService } from '../socket/socket.service';
import { PageLoaderService } from '../page-loader-service/page-loader.service';
import { MatSnackBar } from '@angular/material';

@Component({
    selector: 'app-stream',
    templateUrl: './stream.component.html',
    styleUrls: ['./stream.component.scss']
})
export class StreamComponent implements OnInit, OnDestroy {

    public loading = false;
    public url?: string;
    public streamHistory: IStream[] = [];

    /**
     * Creates an instance of StreamComponent.
     * @memberof StreamComponent
     */
    constructor(
        private pageLoader: PageLoaderService,
        private socket: SocketService,
        private snackBar: MatSnackBar
    ) { }

    /**
     * Holds an arrow function that handles the stream history event
     * @private
     * @param {IStream[]} history list of the streams
     * @memberof StreamComponent
     */
    private onStreamHistory = (history: IStream[]) => {
        this.streamHistory = history;
        setTimeout(() => {
            this.loading = false;
        }, 500);
    }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof StreamComponent
     */
    public ngOnInit() {
        this.loading = true;

        this.socket
            .subscribe('stream history', this.onStreamHistory);

        // send an event message for the list of the stream history
        this.socket
            .emit('stream history');
    }

    /**
     * Implementation of the ngOnDestroy method, of the OnDestroy base class
     * @memberof StreamComponent
     */
    public ngOnDestroy() {
        this.socket
            .unsubscribe('stream history', this.onStreamHistory);
    }

    /**
     * Request a load stream to the server
     * @param {string} url that is requested for playback
     * @memberof StreamComponent
     */
    public onRequestStream(url?: string) {
        if (url) {
            this.pageLoader.start();
            this.socket.emit('load stream', url);
            this.url = undefined;
        } else {
            this.snackBar
                .open('Invalid Url', '', { duration: 2000 })
        }
    }

    /**
     * Request a load registeres stream to the server
     * @param {IStream} stream information to be loaded
     * @memberof StreamComponent
     */
    public onLoad(stream: IStream) {
        if (stream && stream.url) {
            this.pageLoader.start();
            this.socket.emit('load stream', stream.url);
        }
    }

    /**
     * Request the stream history
     * @memberof StreamComponent
     */
    public onRefresh() {
        this.loading = true;
        this.socket.emit('stream history');
    }

}
