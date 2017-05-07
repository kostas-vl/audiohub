import { Component, Input, ViewChild, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { MdSidenav } from '@angular/material';
import { SocketService } from './socket/socket.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

    @ViewChild('sidenav')
    public sidenav: MdSidenav;

    constructor(
        private router: Router,
        private socket: SocketService
    ) { }

    public ngOnInit() {
        this.socket.connect();
    }

    public ngOnDestroy() {
        this.socket.disconnect();
    }

    public onItemClick(url: string) {
        if (url) {
            this.sidenav.toggle();
            this.router.navigateByUrl(url);
        }
    }

}
