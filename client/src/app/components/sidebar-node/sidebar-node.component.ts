import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { SidebarNode } from 'src/app/models/sidebar-node';
import { SidebarService } from 'src/app/services/sidebar/sidebar.service';

/**
 * This class represents an angular component that displays a sidebar node to the user.
 * @export
 * @class SidebarNodeComponent
 */
@Component({
    selector: 'app-sidebar-node',
    templateUrl: './sidebar-node.component.html',
    styleUrls: ['./sidebar-node.component.scss']
})
export class SidebarNodeComponent implements OnInit {

    @Input()
    public node?: SidebarNode;

    public get children() {
        return this.node?.children || [];
    }

    /**
     * Creates a new instance of SidebaseNodeComponent.
     * @memberof SidebarNodeComponent
     */
    constructor(
        private router: Router,
        private sidebarService: SidebarService
    ) { }

    /**
     * Executes any necessary start up code for the component.
     * @memberof SidebarNodeComponent
     */
    public ngOnInit() { }

    /**
     * Handles the sidenav child item click event.
     * @params {string} url The url the user will be navigated to.
     * @memberof SidebarNodeComponent
     */
    public onNavigateToUrl(url: string) {
        this.router.navigateByUrl(url);
        this.sidebarService.toggle();
    }

}
