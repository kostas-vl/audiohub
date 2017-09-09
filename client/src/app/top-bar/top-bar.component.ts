import { Component, OnInit, Input } from '@angular/core';
import { PageLoaderService } from '../page-loader-service/page-loader.service';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-top-bar',
    templateUrl: './top-bar.component.html',
    styleUrls: ['./top-bar.component.scss']
})
export class TopBarComponent implements OnInit {

    @Input()
    public sidenav: any;

    /**
     * Creates an instance of TopBarComponent.
     * @memberof TopBarComponent
     */
    constructor(
        private pageLoader: PageLoaderService,
        private socket: SocketService
    ) { }

    /**
     * Holds an arrow function that handles the mount volume success event
     * @private
     * @memberof TopBarComponent
     */
    private onMountVolumeSuccess = _ => {
        this.pageLoader.stop();
    }

    /**
     * Holds an arrow function that handles the mount volume failure event
     * @private
     * @memberof TopBarComponent
     */
    private onMountVolumeFailure = _ => {
        this.pageLoader.stop();
    }

    /**
     * Holds an arrow function that handles the add volume success event
     * @private
     * @memberof TopBarComponent
     */
    private onAddVolumeSuccess = _ => {
        this.pageLoader.stop();
    }

    /**
     * Holds an arrow function that handles the add volume failure event
     * @private
     * @memberof TopBarComponent
     */
    private onAddVolumeFailure = _ => {
        this.pageLoader.stop();
    }

    /**
     * Holds an arrow function that handles the load stream complete event
     * @private
     * @memberof TopBarComponent
     */
    private onLoadStreamComplete = _ => {
        setTimeout(() => {
            this.pageLoader.stop();
        }, 1500);
    }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof TopBarComponent
     */
    ngOnInit() {
        this.socket
            .subscribe('mount volume success', this.onMountVolumeSuccess);

        this.socket
            .subscribe('mount volume failure', this.onMountVolumeFailure);

        this.socket
            .subscribe('add volume success', this.onAddVolumeSuccess);

        this.socket
            .subscribe('add volume failure', this.onAddVolumeFailure);

        this.socket
            .subscribe('load stream complete', this.onLoadStreamComplete);
    }

}
