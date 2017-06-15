import { Injectable } from '@angular/core';
import { PlatformLocation } from '@angular/common';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import * as io from 'socket.io-client';

@Injectable()
export class SocketService {

    public socketInstance: SocketIOClient.Socket;

    public constructor(private platform: PlatformLocation) {

    }

    public connect() {
        if (!this.socketInstance) {
            if (!environment.webSocketUrl) {
                environment.webSocketUrl = 'ws://' + (this.platform as any).location.origin + '/server';
            }
            this.socketInstance = io.connect(environment.webSocketUrl);
        }
    }

    public disconnect() {
        this.socketInstance.disconnect();
    }

    public subscribe(event: string, callback: (response: any) => void) {
        this.socketInstance.on(event, callback);
    }

    public send(data: string) {
        this.socketInstance.send(data);
    }

    public emit(event: string, data: any = undefined) {
        this.socketInstance.emit(event, data);
    }

}
