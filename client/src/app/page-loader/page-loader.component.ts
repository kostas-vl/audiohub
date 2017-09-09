import { Component, OnInit } from '@angular/core';
import { PageLoaderService } from '../page-loader-service/page-loader.service';

@Component({
    selector: 'app-page-loader',
    templateUrl: './page-loader.component.html',
    styleUrls: ['./page-loader.component.scss']
})
export class PageLoaderComponent implements OnInit {

    public loading = false;

    /**
     * Creates an instance of PageLoaderComponent.
     * @memberof PageLoaderComponent
     */
    constructor(private pageLoader: PageLoaderService) { }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() {
        // create a loader start callback
        this.pageLoader.onStart(() => this.loading = true);
        // create a loader stop callback
        this.pageLoader.onStop(() => this.loading = false);
    }

}
