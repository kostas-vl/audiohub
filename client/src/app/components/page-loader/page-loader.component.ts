import { Component, OnInit } from '@angular/core';
import { PageLoaderService } from 'src/app/services/page-loader/page-loader.service';

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
     * Executes the necessary start up code for the component.
     * @memberof PageLoaderComponent
     */
    public ngOnInit() {
        this.pageLoader.onStart(() => this.loading = true);
        this.pageLoader.onStop(() => this.loading = false);
    }

}
