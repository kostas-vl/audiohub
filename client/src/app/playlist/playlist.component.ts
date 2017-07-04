import { Component, OnInit } from '@angular/core';
import { IPlaylist, Playlist, Playlist2, Playlist3 } from '../models/playlist';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-playlist',
    templateUrl: './playlist.component.html',
    styleUrls: ['./playlist.component.css']
})
export class PlaylistComponent implements OnInit {

    public loading: boolean;
    public playlist: IPlaylist[] = [];
    public streamSource: any = null;

    constructor(private socket: SocketService) { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
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
     * refreshes the entries on the displayed playlist
     */
    public onRefresh() {
        this.socket.emit('queue');
    }

    /**
     * start playing the entire playlist
     */
    public onPlaylistPlay() {
        this.socket.emit('play all');
    }

    /**
     * removes an entry from the playlist
     */
    public onRemove(entry: IPlaylist) {
        this.socket.emit('queue pop', entry.identity);
    }

    /**
     * starts playing the provided track, immediately
     * @param {IPlaylist} entry to start playing
     */
    public onPlayNow(entry: IPlaylist) {
        this.socket.emit('play', entry);
        // this.socket.emit('channel stream', entry);
    }

}
