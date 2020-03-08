import { Component, OnInit } from '@angular/core';
import { IMountFolder, MountFolder } from 'src/app/models/mount-folder';
import { ILocalFolder, LocalFolder } from 'src/app/models/local-folder';
import { SocketService } from 'src/app/services/socket/socket.service';

@Component({
    selector: 'app-systems',
    templateUrl: './systems.component.html',
    styleUrls: ['./systems.component.scss']
})
export class SystemsComponent implements OnInit {

    public mountFolder: IMountFolder = new MountFolder();

    public folder: ILocalFolder = new LocalFolder();

    public addOptions = [
        {
            label: 'Mount Network Folder',
            value: 0
        },
        {
            label: 'Add Local Folder',
            value: 1
        }
    ];

    /**
     * Creates an instance of SystemsComponent.
     * @memberof SystemsComponent
     */
    constructor(private socket: SocketService) { }

    /**
     * Implementation of the ngOnInit method, of the OnInit base class
     * @memberof SystemsComponent
     */
    public ngOnInit() { }

    /**
     * Executes the proper event for the selected tab
     * @param {number} index of the selected tab
     * @memberof SystemsComponent
     */
    public onComplete(index: number) {
        switch (index) {
            case 0:
                this.socket.emit('mount volume', this.mountFolder);
                this.mountFolder = new MountFolder();
                break;

            case 1:
                this.socket.emit('add volume', this.folder);
                this.folder = new LocalFolder();
                break;

            default:
                break;
        }
    }

}
