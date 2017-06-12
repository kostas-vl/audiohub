import { Component, Input, ViewChild, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { MdSidenav, MdSnackBar } from '@angular/material';
import { ISettings } from './models/settings';
import { SocketService } from './socket/socket.service';
import { SettingsService } from './settings-service/settings.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

    private settingsSubscription: number;
    public settings: ISettings;
    public addDialogShow = false;
    public addDialogLoading = false;

    @ViewChild('sidenav')
    public sidenav: MdSidenav;

    constructor(
        private router: Router,
        private socket: SocketService,
        private settingsService: SettingsService,
        private snackbar: MdSnackBar
    ) { }

    public ngOnInit() {
        this.settings = this.settingsService.get();
        this.settingsSubscription = this.settingsService.subscribe(settings => {
            this.settings = settings;
        });
        this.socket.connect();

        this.socket.subscribe('mount volume success', _ => {
            this.snackbar.open('Volume mounted!', '', { duration: 1500 });
            this.addDialogLoading = false;
        });

        this.socket.subscribe('add volume success', _ => {
            this.snackbar.open('Volume added!', '', { duration: 1500 });
            this.addDialogLoading = false;
        });

        this.socket.subscribe('download finished', data => {
            this.snackbar.open('Download finished!', '', { duration: 1500 });
            this.addDialogLoading = false;
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

    public onOpenDialog() {
        this.addDialogShow = true;
    }

    public onCloseDialog() {
        this.addDialogShow = false;
    }

    public onDialogComplete(data: any) {
        if (data) {
            this.onCloseDialog();
            this.addDialogLoading = true;
            this.socket.emit(data.action, data.details);
        }
    }

}
