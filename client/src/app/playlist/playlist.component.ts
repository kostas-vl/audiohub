import { Component, OnInit, OnDestroy } from '@angular/core';
import { IPlaylist, Playlist, Playlist2, Playlist3 } from '../models/playlist';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-playlist',
    templateUrl: './playlist.component.html',
    styleUrls: ['./playlist.component.scss']
})
export class PlaylistComponent implements OnInit, OnDestroy {

    public loading: boolean;
    public playlist: IPlaylist[] = [];
    public streamSource: any = null;

    /**
     * Creates an instance of PlaylistComponent.
     * @memberof PlaylistComponent
     */
    constructor(private socket: SocketService) { }

    /**
     * Holds an arrow function that handles the on queue event
     * @private
     * @param {IPlaylist[]} data queued on the playlist
     * @memberof PlaylistComponent
     */
    private onQueue = (data: IPlaylist[]) => {
        this.playlist = data;
        this.loading = false;
    }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof PlaylistComponent
     */
    public ngOnInit() {
        this.loading = true;

        this.socket
            .subscribe('queue', this.onQueue);

        // sends an event message for the current playlist queue
        this.socket
            .emit('queue');
    }

    /**
     * Implementation of the ngOnDestroy method, of the OnDestroy base class
     * @memberof PlaylistComponent
     */
    public ngOnDestroy() {
        this.socket
            .unsubscribe('queue', this.onQueue);
    }

    /**
     * Refreshes the entries on the displayed playlist
     * @memberof PlaylistComponent
     */
    public onRefresh() {
        this.socket.emit('queue');
    }

    /**
     * Start playing the entire playlist
     * @memberof PlaylistComponent
     */
    public onPlaylistPlay() {
        this.socket.emit('play all');
    }

    /**
     * Removes an entry from the playlist
     * @param {IPlaylist} entry of the playlist to be removed
     * @memberof PlaylistComponent
     */
    public onRemove(entry: IPlaylist) {
        this.socket.emit('queue pop', entry.identity);
    }

    /**
     * Starts playing the provided track, immediately
     * @param {IPlaylist} entry of the playlist to be played immediately
     * @memberof PlaylistComponent
     */
    public onPlayNow(entry: IPlaylist) {
        this.socket.emit('play', entry);
    }

}
