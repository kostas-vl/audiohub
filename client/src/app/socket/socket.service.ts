import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';

@Injectable()
export class SocketService {

  public socketInstance: SocketIOClient.Socket;

    public constructor() { }

    public connect() {
        if (!this.socketInstance) {
            this.socketInstance = io.connect('ws://127.0.0.1:5000/server');
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
