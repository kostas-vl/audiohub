import { Injectable } from '@angular/core';
import { SocketService } from '../socket/socket.service';

@Injectable()
export class PageLoaderService {

    private startCallback: () => void;
    private stopCallback: () => void;

    constructor(private socket: SocketService) { }

    public onStart(callback: () => void) {
        if (callback) {
            this.startCallback = callback;
        }
    }

    public onStop(callback: () => void) {
        if (callback) {
            this.stopCallback = callback;
        }
    }

    public start() {
        this.startCallback();
    }

    public stop() {
        this.stopCallback();
    }

}
