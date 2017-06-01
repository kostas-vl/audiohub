import { Component, Input, ViewChild, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { MdSidenav, MdSnackBar } from '@angular/material';
import { SocketService } from './socket/socket.service';
import { SettingsService } from './settings-service/settings.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

    private settingsSubscription: number;
    public darkTheme: boolean;

    @ViewChild('sidenav')
    public sidenav: MdSidenav;

    constructor(
        private router: Router,
        private socket: SocketService,
        private settingsService: SettingsService,
        private snackbar: MdSnackBar
    ) { }

    public ngOnInit() {
        this.darkTheme = this.settingsService.get().darkTheme;
        this.settingsSubscription = this.settingsService.subscribe(settings => this.darkTheme = settings.darkTheme);
        this.socket.connect();
        this.socket.subscribe('download finished', data => {
            this.snackbar.open('Download finished!', '', { duration: 1500, extraClasses: ['snack-bar-bg'] });
        });
    }

    public ngOnDestroy() {
        this.settingsService.unsubscribe(this.settingsSubscription);
        this.socket.disconnect();
    }

    public onItemClick(url: string) {
        if (url) {
            this.sidenav.toggle();
            this.router.navigateByUrl(url);
        }
    }

}
