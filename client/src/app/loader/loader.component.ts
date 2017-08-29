import { Component, Input } from '@angular/core';

@Component({
    selector: 'app-loader',
    templateUrl: './loader.component.html',
    styleUrls: ['loader.component.scss']
})
export class LoaderComponent {

    @Input()
    public loading: boolean;

    @Input()
    public height = '250px';

    @Input()
    public width = '100%';

    constructor() { }

}
