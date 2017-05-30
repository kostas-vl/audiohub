import { Component, OnInit } from '@angular/core';
import { IPlaylist } from '../models/playlist';
import { SocketService } from '../socket/socket.service';
import { IPlayerInfo, PlayerInfo } from '../models/player-info';

@Component({
    selector: 'app-player',
    templateUrl: './player.component.html',
    styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit {

    public progressValue = 0;
    public progressBuffer = 0;
    public progressMode: 'indeterminate' | 'determinate' | 'buffer' | 'query' = 'determinate';
    public info: IPlayerInfo = new PlayerInfo();

    constructor(private socket: SocketService) { }

    private setProgressMode(state: 'init' | 'playing' | 'paused' | 'stoped') {
        switch (state) {
            case 'playing':
                this.progressMode = 'buffer';
                break;
            case 'paused':
            case 'stoped':
                this.progressMode = 'determinate';
                break;
            case 'init':
            default:
                break;
        }
    }

    public ngOnInit() {
        this.socket.subscribe('player info', (info: IPlayerInfo) => {
            this.info = info;
            this.setProgressMode(this.info.state);
        });
        this.socket.emit('player info');
    }

    public onPlay() {
        this.socket.emit('play');
        this.info.state = 'playing';
        this.setProgressMode(this.info.state);
    }

    public onPause() {
        this.socket.emit('pause');
        this.info.state = 'paused';
        this.setProgressMode(this.info.state);
    }

    public onStop() {
        this.socket.emit('stop');
        this.info.state = 'stoped';
        this.setProgressMode(this.info.state);
    }

    public onNext() {
        this.socket.emit('next');
    }

    public onVolume(value: number) {
        this.socket.emit('volume', value);
    }

}
