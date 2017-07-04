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

    /**
     * sets the proper value on the progres mode property, based on the provided state
     * @param {string} state of the progress bar
     */
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

    /**
     * implementation of the ngOnInit method of the OnInit base class
     */
    public ngOnInit() {
        // subscribe an event handler for the 'player info' event
        this.socket.subscribe('player info', (info: IPlayerInfo) => {
            this.info = info;
            this.setProgressMode(this.info.state);
        });
        // subscribe an event handler for the 'channel stream' event
        this.socket.subscribe('channel stream', (buffer: ArrayBuffer) => {
            // creating the audio context
            const context = new AudioContext();

            const container = {
                data: Array.apply(null, new Uint32Array(buffer)),
                contentType: 'audio/x-wav'
            };
            const typedData = JSON.parse(JSON.stringify(container));
            const typedBuffer = new Uint32Array(typedData.data).buffer;

            // decoding the audio data and handling the success and error events
            context
                .decodeAudioData(typedBuffer)
                .then((audioBuffer: AudioBuffer) => {
                    // create a new buffer source
                    const node = context.createBufferSource();

                    // assign the audio buffer to the source bufer
                    node.buffer = audioBuffer;

                    // connect to the context destination
                    node.connect(context.destination);

                    // start playback
                    node.start(0);
                })
                .catch(reason => console.log(reason));
        });
        // sends an event message for the current state of the player, on the server
        this.socket.emit('player info');
    }

    /**
     * sends an event message for the player, on the server, to start playing
     */
    public onPlay() {
        this.socket.emit('play');
        this.info.state = 'playing';
        this.setProgressMode(this.info.state);
    }

    /**
     * sends an event message for the player, on the server, to pause
     */
    public onPause() {
        this.socket.emit('pause');
        this.info.state = 'paused';
        this.setProgressMode(this.info.state);
    }

    /**
     * sends an event message for the player, on the server, to stop playing
     */
    public onStop() {
        this.socket.emit('stop');
        this.info.state = 'stoped';
        this.setProgressMode(this.info.state);
    }

    /**
     * sends an event message for the player, on the server, to go back to the previous track
     */
    public onPrevious() {
        this.socket.emit('previous');
    }

    /**
     * sends an event message for the player, on the server, to skip the current track
     */
    public onNext() {
        this.socket.emit('next');
    }

    /**
     * sends an event message for the player, on the server, to adjust the volume
     * @param {number} value for the volume of the player
     */
    public onVolume(value: number) {
        this.socket.emit('volume', value);
    }

}
