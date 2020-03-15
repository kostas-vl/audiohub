import { Component, OnInit } from '@angular/core';
import { SidebarNode } from 'src/app/models/sidebar-node';

/**
 * This class represents an angular component that displays to the user a sidebar
 * navigatio menu.
 * @export
 * @class SidebarComponent
 */
@Component({
    selector: 'app-sidebar',
    templateUrl: './sidebar.component.html',
    styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {

    public nodes: SidebarNode[] = [
        {
            text: 'Home',
            isHeader: true,
            children: [
                {
                    icon: 'album',
                    text: 'Playlist',
                    url: '/playlist',
                    isHeader: false
                }
            ]
        },
        {
            text: 'Music',
            isHeader: true,
            children: [
                {
                    icon: 'insert_drive_file',
                    text: 'Files',
                    url: '/files',
                    isHeader: false
                },
                {
                    icon: 'airplay',
                    text: 'Streams',
                    url: '/stream',
                    isHeader: false
                }
            ]
        },
        {
            text: 'Storage',
            isHeader: true,
            children: [
                {
                    icon: 'settings_system_daydream',
                    text: 'Systems',
                    url: '/download',
                    isHeader: false
                },
                {
                    icon: 'file_download',
                    text: 'Download',
                    url: '/download',
                    isHeader: false
                }
            ]
        },
        {
            text: 'Settings',
            isHeader: true,
            children: [
                {
                    icon: 'invert_colors',
                    text: 'Appearence',
                    url: '/settings',
                    isHeader: false
                }
            ]
        }
    ];

    /**
     * Creates a new instance of SidebarComponent.
     * @memberof SidebarComponent
     */
    constructor() { }

    /**
     * Executes any necessary start up code for the component.
     * @memberof SidebarComponent
     */
    public ngOnInit() { }

}
