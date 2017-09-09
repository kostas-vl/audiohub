import { Component, OnInit } from '@angular/core';
import { IPlaylist, Playlist, Playlist2, Playlist3 } from '../models/playlist';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-playlist',
    templateUrl: './playlist.component.html',
    styleUrls: ['./playlist.component.scss']
})
export class PlaylistComponent implements OnInit {

    public loading: boolean;
    public playlist: IPlaylist[] = [];
    public streamSource: any = null;

    /**
     * Creates an instance of PlaylistComponent.
     * @memberof PlaylistComponent
     */
    constructor(private socket: SocketService) { }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof PlaylistComponent
     */
    public ngOnInit() {
        // displays the loader
        this.loading = true;
        // subscribes an event handler on the 'queue' event
        this.socket.subscribe('queue', data => {
            this.playlist = data;
            this.loading = false;
        });
        // sends an event message for the current playlist queue
        this.socket.emit('queue');
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
     * @param {IPlaylist} entry 
     * @memberof PlaylistComponent
     */
    public onRemove(entry: IPlaylist) {
        this.socket.emit('queue pop', entry.identity);
    }

    /**
     * Starts playing the provided track, immediately
     * @param {IPlaylist} entry 
     * @memberof PlaylistComponent
     */
    public onPlayNow(entry: IPlaylist) {
        this.socket.emit('play', entry);
    }

}
