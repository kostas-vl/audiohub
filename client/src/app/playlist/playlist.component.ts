import { Component, OnInit } from '@angular/core';
import { IPlaylist } from '../models/playlist';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-playlist',
    templateUrl: './playlist.component.html',
    styleUrls: ['./playlist.component.css']
})
export class PlaylistComponent implements OnInit {

    public loading: boolean;
    public playlist: IPlaylist[] = [];

    constructor(private socket: SocketService) { }

    public ngOnInit() {
        this.loading = true;
        this.socket.subscribe('queue', data => {
            this.playlist = data;
            this.loading = false;
        });
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
