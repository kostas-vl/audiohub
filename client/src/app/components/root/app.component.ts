import { Component, Input, ViewChild, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ISettings, Settings } from 'src/app/models/settings';
import { SocketService } from 'src/app/services/socket/socket.service';
import { SettingsService } from 'src/app/services/settings/settings.service';
import { PageLoaderService } from 'src/app/services/page-loader/page-loader.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {

    private settingsSubscription?: number;

    public settings: ISettings = new Settings();

    @ViewChild(MatSidenav, { static: true })
    public sidenav?: MatSidenav;

    /**
     * Creates an instance of AppComponent.
     * @memberof AppComponent
     */
    constructor(
        private router: Router,
        private pageLoader: PageLoaderService,
        private socket: SocketService,
        private settingsService: SettingsService,
        private snackbar: MatSnackBar
    ) { }

    /**
     * Holds an arrow function that handles the mount volume success event
     * @private
     * @memberof AppComponent
     */
    private onMountVolumeSuccess = (response: any) => {
        this.pageLoader.stop();
        this.snackbar.open('Volume mounted!', '', { duration: 2000 });
    }

    /**
     * Holds an arrow function that handles the mount volume failure event
     * @private
     * @memberof AppComponent
     */
    private onMountVolumeFailure = (response: any) => {
        this.pageLoader.stop();
        this.snackbar.open('An error occured!', '', { duration: 2000 });
    }

    /**
     * Holds an arrow function that handles the add volume success event
     * @private
     * @memberof AppComponent
     */
    private onAddVolumeSuccess = (response: any) => {
        this.pageLoader.stop();
        this.snackbar.open('Volume added!', '', { duration: 2000 });
    }

    /**
     * Holds an arrow function that handles the add volume failure event
     * @private
     * @memberof AppComponent
     */
    private onAddVolumeFailure = (response: any) => {
        this.pageLoader.stop();
        this.snackbar.open('An error occured', '', { duration: 2000 });
    }

    /**
     * Holds an arrow function that handles the download finished event
     * @private
     * @memberof AppComponent
     */
    private onDownloadFinished = (response: any) => {
        this.pageLoader.stop();
        this.snackbar.open('Download finished!', '', { duration: 2000 });
    }

    /**
     * Holds an arrow function that handles the load stream complete event
     * @private
     * @memberof AppComponent
     */
    private onLoadStreamComplete = (response: any) => {
        this.pageLoader.stop();
        this.snackbar.open('Stream Loaded!', '', { duration: 2000 });
    }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof AppComponent
     */
    public ngOnInit() {
        // initialize the settigns model
        this.settings = this.settingsService.get();

        // subscribe a callback on the event of a settings change, and store the produced index
        this.settingsSubscription = this
            .settingsService
            .subscribe(settings => {
                this.settings = settings;
            });

        // connect to the server socket and subscribe to all the neccessary events
        this.socket.connect();

        this.settingsService.configure();

        this.socket.subscribe('connect', () => {
            this.socket.subscribe('mount volume success', this.onMountVolumeSuccess);

            this.socket.subscribe('mount volume failure', this.onMountVolumeFailure);

            this.socket.subscribe('add volume success', this.onAddVolumeSuccess);

            this.socket.subscribe('add volume failure', this.onAddVolumeFailure);

            this.socket.subscribe('download finished', this.onDownloadFinished);

            this.socket.subscribe('load stream complete', this.onLoadStreamComplete);

            // send request for the settings of the user
            this.socket.emit('user settings');
        });

    }

    /**
     * Implements the ngOnDestroy method, of the OnDestroy base class
     * @memberof AppComponent
     */
    public ngOnDestroy() {
        // remove all the subscription callbacks
        this.settingsService.unsubscribe(this.settingsSubscription);

        this.socket.unsubscribe('mount volume success', this.onMountVolumeSuccess);

        this.socket.unsubscribe('mount volume failure', this.onMountVolumeFailure);

        this.socket.unsubscribe('add volume success', this.onAddVolumeSuccess);

        this.socket.unsubscribe('add volume failure', this.onAddVolumeFailure);

        this.socket.unsubscribe('download finished', this.onDownloadFinished);

        this.socket.unsubscribe('load stream complete', this.onLoadStreamComplete);

        // disconnect from the server socket
        this.socket.disconnect();
    }

    /**
     * Navigates the user to a view of his choices from the list of the sidenav
     * @param {string} url of the new view
     * @memberof AppComponent
     */
    public onSidenavItemClick(url: string) {
        if (url && this.sidenav) {
            this.sidenav.toggle();
            this.router.navigateByUrl(url);
        }
    }

}
