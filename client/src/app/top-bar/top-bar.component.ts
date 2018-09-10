import { Component, OnInit, OnDestroy, Input } from '@angular/core';
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
    constructor() { }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof TopBarComponent
     */
    ngOnInit() { }

}
