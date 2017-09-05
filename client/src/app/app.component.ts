import { Component, Input, ViewChild, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { MdSidenav, MdSnackBar } from '@angular/material';
import { ISettings } from './models/settings';
import { SocketService } from './socket/socket.service';
import { SettingsService } from './settings-service/settings.service';
import { PageLoaderService } from './page-loader-service/page-loader.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {

    private settingsSubscription: number;
    public settings: ISettings;

    @ViewChild('sidenav')
    public sidenav: MdSidenav;

    constructor(
        private router: Router,
        private pageLoader: PageLoaderService,
        private socket: SocketService,
        private settingsService: SettingsService,
        private snackbar: MdSnackBar
    ) { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
     */
    public ngOnInit() {
        // initialize the settigns model
        this.settings = this.settingsService.get();

        // subscribe a callback on the event of a settings change, and store the produced index
        this.settingsSubscription = this.settingsService.subscribe(settings => {
            this.settings = settings;
        });

        // connect to the server socket
        this.socket.connect();

        // configure socket bindings for the settings service
        this.settingsService.configure();

        // subscribe an event handler on the 'mount volume success' event
        this.socket.subscribe('mount volume success', _ => {
            this.snackbar.open('Volume mounted!', '', { duration: 2000 });
        });

        // subscribe an event handler on the 'mount volume failure' event
        this.socket.subscribe('mount volume failure', _ => {
            this.snackbar.open('An error occured!', '', { duration: 2000 });
        });

        // subscribe an event handler on the 'add volume success' event
        this.socket.subscribe('add volume success', _ => {
            this.snackbar.open('Volume added!', '', { duration: 2000 });
        });

        // subscribe an event handler on the 'add volume failure' event
        this.socket.subscribe('add volume failure', _ => {
            this.snackbar.open('An error occured', '', { duration: 2000 });
        });

        // subscribe an event handler on the 'download finished' event
        this.socket.subscribe('download finished', _ => {
            this.snackbar.open('Download finished!', '', { duration: 2000 });
        });

        // subscribe an event handler on the 'stream loaded' event
        this.socket.subscribe('load stream complete', _ => {
            this.snackbar.open('Stream Loaded!', '', { duration: 2000 });
        });

        // send request for the settings of the user
        this.socket.emit('user settings');
    }

    /**
     * implements the ngOnDestroy method, of the OnDestroy base class
     */
    public ngOnDestroy() {
        // remove the subscription callback from the settings service
        this.settingsService.unsubscribe(this.settingsSubscription);

        // disconnect from the server socket
        this.socket.disconnect();
    }

    /**
     * navigates the user to a view of his choices from the list of the sidenav
     * @param {string} url of the new view
     */
    public onSidenavItemClick(url: string) {
        if (url) {
            this.sidenav.toggle();
            this.router.navigateByUrl(url);
        }
    }

}
