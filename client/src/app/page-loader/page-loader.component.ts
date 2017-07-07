import { Component, OnInit } from '@angular/core';
import { PageLoaderService } from '../page-loader-service/page-loader.service';

@Component({
    selector: 'app-page-loader',
    templateUrl: './page-loader.component.html',
    styleUrls: ['./page-loader.component.css']
})
export class PageLoaderComponent implements OnInit {

    public loading = false;

    constructor(private pageLoader: PageLoaderService) { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() {
        // create a loader start callback
        this.pageLoader.onStart(() => this.loading = true);
        // create a loader stop callback
        this.pageLoader.onStop(() => this.loading = false);
    }

}
