import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { PageLoaderService } from 'src/app/services/page-loader/page-loader.service';
import { SocketService } from 'src/app/services/socket/socket.service';

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
    public ngOnInit() { }

}
