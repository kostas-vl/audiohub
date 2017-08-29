import { Component, OnInit, Input } from '@angular/core';

@Component({
    selector: 'app-top-bar',
    templateUrl: './top-bar.component.html',
    styleUrls: ['./top-bar.component.scss']
})
export class TopBarComponent implements OnInit {

    @Input()
    public sidenav: any;

    constructor() { }

    /**
     * implementation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() { }

}
