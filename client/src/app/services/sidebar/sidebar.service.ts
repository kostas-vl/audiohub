import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

/**
 * This class represents an angular service that exposes methods for interacting with the apps
 * sidebar.
 * @export
 * @class SidebarService
 */
@Injectable()
export class SidebarService {

    private sidebarToggleSource = new Subject();

    public sidebarToggle = this.sidebarToggleSource.asObservable();

    /**
     * Creates a new instance of SidebarService.
     * @memberof SidebarService
     */
    constructor() { }

    /**
     * Toggles the sidebar and informs all observers.
     * @memberof SidebarService
     */
    public toggle() {
        this.sidebarToggleSource.next();
    }

}
