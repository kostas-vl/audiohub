import { Component, OnInit } from '@angular/core';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-stream',
    templateUrl: './stream.component.html',
    styleUrls: ['./stream.component.css']
})
export class StreamComponent implements OnInit {

    public url: string;

    constructor(private socket: SocketService) { }

    ngOnInit() { }

    public onRequestStream(url: string) {
        if (url) {
            this.socket.emit('load stream', url);
        }
    }

}
