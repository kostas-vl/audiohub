import { Component, Input, ViewChild, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { MdSidenav, MdSnackBar } from '@angular/material';
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
        private socket: SocketService,
        private snackbar: MdSnackBar
    ) { }

    public ngOnInit() {
        this.socket.connect();
        this.socket.subscribe('download finished', data => {
            this.snackbar.open('Download finished!', '', { duration: 1000, extraClasses: ['snack-bar-bg'] });
        });
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
