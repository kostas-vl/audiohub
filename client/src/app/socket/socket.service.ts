import { Injectable } from '@angular/core';
import { PlatformLocation } from '@angular/common';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import * as io from 'socket.io-client';
import { SoundDirection } from '../models/sound-direction';

@Injectable()
export class SocketService {

    public socketInstance: SocketIOClient.Socket;

    public constructor(private platform: PlatformLocation) { }

    /**
     * creates a connection with the server web socket
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
     * disconnect from the server web socket
     */
    public disconnect() {
        if (this.socketInstance) {
            this.socketInstance.disconnect();
        }
    }

    /**
     * create an event handler for the provided event
     * @param {string} event for the subscription
     * @param callback to be executed
     */
    public subscribe(event: string, callback: (response: any) => void) {
        this.socketInstance.on(event, callback);
    }

    /**
     * sends a message to the server socket
     * @param {string} data to be sent
     */
    public send(data: string) {
        this.socketInstance.send(data);
    }

    /**
     * emits a message and data, to the server socket, based on the provided event name
     * @param {string} event to be emitted
     * @param {any} data to be emitted
     */
    public emit(event: string, data: any = undefined) {
        this.socketInstance.emit(event, data);
    }

}
