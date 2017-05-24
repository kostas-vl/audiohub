import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import * as io from 'socket.io-client';

@Injectable()
export class SocketService {

    public socketInstance: SocketIOClient.Socket;

    public constructor() { }

    public connect() {
        if (!this.socketInstance) {
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
