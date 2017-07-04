import { Component, OnInit } from '@angular/core';
import { MdTabGroup } from '@angular/material';
import { IMountFolder, MountFolder } from '../models/mount-folder';
import { ILocalFolder, LocalFolder } from '../models/local-folder';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-systems',
    templateUrl: './systems.component.html',
    styleUrls: ['./systems.component.css']
})
export class SystemsComponent implements OnInit {

    public tabGroupComponent: MdTabGroup;
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

    constructor(private socket: SocketService) { }

    ngOnInit() { }

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
