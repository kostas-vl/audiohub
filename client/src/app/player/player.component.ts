import { Component, OnInit, OnDestroy } from '@angular/core';
import { IPlaylist } from '../models/playlist';
import { SocketService } from '../socket/socket.service';
import { IPlayerInfo, PlayerInfo } from '../models/player-info';

type TimeTuple = {
    currentTime: number,
    currentTimeStr: string
};

@Component({
    selector: 'app-player',
    templateUrl: './player.component.html',
    styleUrls: ['./player.component.scss']
})
export class PlayerComponent implements OnInit, OnDestroy {

    public progressValue = 0;
    public progressBuffer = 0;
    public progressMode: 'indeterminate' | 'determinate' | 'buffer' | 'query' = 'determinate';
    public info: IPlayerInfo = new PlayerInfo();

    /**
     * Creates an instance of PlayerComponent.
     * @memberof PlayerComponent
     */
    constructor(private socket: SocketService) { }

    /**
     * Sets the appropriate value for the mode of the player progress bar
     * @private
     * @param {('init' | 'stoped' | 'paused' | 'playing')} state of the player
     * @memberof PlayerComponent
     */
    private setProgressMode(state: 'init' | 'stoped' | 'paused' | 'playing') {
        switch (state) {
            case 'playing':
                this.progressMode = 'buffer';
                this.progressBuffer = 0;
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

    /**
     * Holds an arrow function that is the handler for the player info event
     * @private
     * @param {IPlayerInfo} info for the player
     * @memberof PlayerComponent
     */
    private onPlayerInfo = (info: IPlayerInfo) => {
        this.info = info;
        this.setProgressMode(this.info.state);
    }

    /**
     * Holds an arrow function that handles the current time event
     * @private
     * @param {TimeTuple} data that contains information for the current timestamp of the playing track
     * @memberof PlayerComponent
     */
    private onCurrentTime = (data: TimeTuple) => {
        this.info.currentTime = data.currentTime;
        this.info.currentTimeStr = data.currentTimeStr;
        this.progressValue = (this.info.currentTime / this.info.time) * 100;
    }

    /**
     * Implementation of the ngOnInit method of the OnInit base class
     * @memberof PlayerComponent
     */
    public ngOnInit() {
        // subscribe an event handler for the 'player info' event
        this.socket
            .subscribe('player info', this.onPlayerInfo);

        // subscribe an event handler for the 'current time' event
        this.socket
            .subscribe('current time', this.onCurrentTime);

        // sends an event message for the current state of the player, on the server
        this.socket
            .emit('player info');
        // create a timer point to request the curernt time of the playback
        // setInterval(() => {
        //     if (this.info.state === 'playing') {
        //         this.socket.emit('current time');
        //     }
        // }, 1000);
    }

    /**
     * Implementation of the ngOnInit method, of the OnDestroy base class
     * @memberof PlayerComponent
     */
    public ngOnDestroy() {
        // Unsubscribe from all the message events
        this.socket
            .unsubscribe('player info', this.onPlayerInfo);

        this.socket
            .unsubscribe('current time', this.onCurrentTime);
    }

    /**
     * Sends an event message for the player, on the server, to start playing
     * @memberof PlayerComponent
     */
    public onPlay() {
        this.socket.emit('play');
        this.info.state = 'playing';
        this.setProgressMode(this.info.state);
    }

    /**
     * Sends an event message for the player, on the server, to pause
     * @memberof PlayerComponent
     */
    public onPause() {
        this.socket.emit('pause');
        this.info.state = 'paused';
        this.setProgressMode(this.info.state);
    }

    /**
     * Sends an event message for the player, on the server, to stop playing
     * @memberof PlayerComponent
     */
    public onStop() {
        this.socket.emit('stop');
        this.info.state = 'stoped';
        this.setProgressMode(this.info.state);
    }

    /**
     * Sends an event message for the player, on the server, to go back to the previous track
     * @memberof PlayerComponent
     */
    public onPrevious() {
        this.socket.emit('previous');
    }

    /**
     * Sends an event message for the player, on the server, to skip the current track
     * @memberof PlayerComponent
     */
    public onNext() {
        this.socket.emit('next');
    }

    /**
     * Sends an event message for the player, on the server, to adjust the volume
     * @param {number} value for the volume of the player
     * @memberof PlayerComponent
     */
    public onVolume(value: number) {
        this.socket.emit('volume', value);
    }

}
