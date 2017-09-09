import { Injectable } from '@angular/core';
import { PlatformLocation } from '@angular/common';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import * as io from 'socket.io-client';
import { SoundDirection } from '../models/sound-direction';

@Injectable()
export class SocketService {

    public socketInstance: SocketIOClient.Socket;

    /**
     * Creates an instance of SocketService.
     * @memberof SocketService
     */
    public constructor(private platform: PlatformLocation) { }

    /**
     * Creates a connection with the server web socket
     * @memberof SocketService
     */
    public connect() {
        // if the socket hasnt been assigned yet
        if (!this.socketInstance) {
            // if there is no web socket url on the enviroment, set the target on the url on the users browser
            // (code path for production so that the server ip is know at runtime)
            if (!environment.webSocketUrl) {
                environment.webSocketUrl = 'ws://' + (this.platform as any).location.host + '/server';
            }
            // connect and assing the produces socket object
            this.socketInstance = io.connect(environment.webSocketUrl, { transports: ['websocket'] });
        }
    }

    /**
     * Disconnect from the server web socket
     * @memberof SocketService
     */
    public disconnect() {
        if (this.socketInstance) {
            this.socketInstance.disconnect();
        }
    }

    /**
     * Create an event handler for the provided event
     * @param {string} event for the subscription
     * @param {(response: any) => void} callback to be executed
     * @memberof SocketService
     */
    public subscribe(event: string, callback: (response: any) => void) {
        this.socketInstance.on(event, callback);
    }

    /**
     * Sends a message to the server socket
     * @param {string} data to be sent
     * @memberof SocketService
     */
    public send(data: string) {
        this.socketInstance.send(data);
    }

    /**
     * Emits a message and data, to the server socket, based on the provided event name
     * @param {string} event to be emitted
     * @param {*} [data=undefined] to be emitted
     * @memberof SocketService
     */
    public emit(event: string, data: any = undefined) {
        this.socketInstance.emit(event, data);
    }

    /**
     * Removes the provided callback from the present event
     * @param {string} event to target
     * @param {Function} callback to be removed
     * @memberof SocketService
     */
    public unsubscribe(event: string, callback: Function) {
        this.socketInstance.removeEventListener(event, callback);
    }

}
