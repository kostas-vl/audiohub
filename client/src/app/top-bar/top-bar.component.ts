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

    constructor(
        private pageLoader: PageLoaderService,
        private socket: SocketService
    ) { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() {
        this.socket
            .subscribe('mount volume success', _ => {
                this.pageLoader.stop();
            });

        this.socket
            .subscribe('add volume success', _ => {
                this.pageLoader.stop();
            });

        this.socket
            .subscribe('load stream complete', _ => {
                setTimeout(() => {
                    this.pageLoader.stop();
                }, 1500);
            });
    }

}
