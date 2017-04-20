import { Component, OnInit } from '@angular/core';
import { SocketService } from '../socket/socket.service';
import { IPlaylist } from '../models/playlist';

@Component({
    selector: 'app-player',
    templateUrl: './player.component.html',
    styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit {

    public progressValue = 0;
    public progressBuffer = 0;
    public progressMode: 'indeterminate' | 'determinate' | 'buffer' | 'query' = 'determinate';
    public volume = 100;
    public playing = false;
    public currentPlaying: IPlaylist;

    constructor(private socket: SocketService) { }

    public ngOnInit() {
        this.socket.subscribe('currently playing', (entry: IPlaylist) => {
            this.playing = true;
            this.progressMode = 'buffer';
            this.currentPlaying = entry;
        });
    }

    public onPlay() {
        this.socket.emit('play');
        this.playing = true;
        this.progressMode = 'buffer';
    }

    public onPause() {
        this.socket.emit('pause');
        this.playing = false;
        this.progressMode = 'determinate';
    }

    public onStop() {
        this.socket.emit('stop');
        this.playing = false;
        this.progressMode = 'determinate';
    }

    public onVolume(value: number) {
        this.socket.emit('volume', value);
    }

}
