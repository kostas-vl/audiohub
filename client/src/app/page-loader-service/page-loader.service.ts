import { Injectable } from '@angular/core';
import { SocketService } from '../socket/socket.service';

@Injectable()
export class PageLoaderService {

    private startCallback?: () => void;
    private stopCallback?: () => void;

    /**
     * Creates an instance of PageLoaderService.
     * @memberof PageLoaderService
     */
    constructor(private socket: SocketService) { }

    /**
     * Registers a callback for the event of the page loader starting
     * @param {() => void} callback to be executed
     * @memberof PageLoaderService
     */
    public onStart(callback: () => void) {
        if (callback) {
            this.startCallback = callback;
        }
    }

    /**
     * Registers a callback for the event of the page loader stoping
     * @param {() => void} callback to be executed
     * @memberof PageLoaderService
     */
    public onStop(callback: () => void) {
        if (callback) {
            this.stopCallback = callback;
        }
    }

    /**
     * Displays the page loader
     * @memberof PageLoaderService
     */
    public start() {
        if (this.startCallback) {
            this.startCallback();
        }
    }

    /**
     * Hides the page loader
     * @memberof PageLoaderService
     */
    public stop() {
        if (this.stopCallback) {
            this.stopCallback();
        }
    }

}
