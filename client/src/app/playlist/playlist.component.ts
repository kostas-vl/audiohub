import { Component, OnInit } from '@angular/core';
import { SocketService } from 'app/socket/socket.service';

import { IPlaylist, Playlist } from 'app/models/playlist';

@Component({
    selector: 'app-playlist',
    templateUrl: './playlist.component.html',
    styleUrls: ['./playlist.component.css']
})
export class PlaylistComponent implements OnInit {

    public playlist: IPlaylist[] = [];

    constructor(private socket: SocketService) { }

    public ngOnInit() {
        this.socket.subscribe('queue', data => this.playlist = data);
        this.socket.emit('queue');
    }

    public onRefresh() {
        this.socket.emit('queue');
    }

    public onPlaylistPlay() {
        this.socket.emit('play all');
    }

    public onRemove(entry: IPlaylist) {
        this.socket.emit('queue pop', entry.id);
    }

    public onPlayNow(entry: IPlaylist) {
        this.socket.emit('play now', entry);
    }

}
