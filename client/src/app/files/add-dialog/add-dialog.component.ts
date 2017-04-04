import { Component, OnInit } from '@angular/core';
import { MdDialogRef } from '@angular/material';
import { SocketService } from 'app/socket/socket.service';
import { IMountFolder, MountFolder } from 'app/files/add-dialog/models/mount-folder';

@Component({
    selector: 'app-add-dialog',
    templateUrl: './add-dialog.component.html',
    styleUrls: ['./add-dialog.component.css']
})
export class AddDialogComponent {

    public addOptions = [
        {
            label: 'Mount Network Folder',
            value: 0
        },
        {
            label: 'Add Local Folder',
            value: 1
        },
        {
            label: 'Download',
            value: 2
        }
    ];

    public selectedAction = 0;

    public mountFolder: IMountFolder = new MountFolder();

    public folder = { name: '', path: '' };

    public downloadDetails = { path: '', url: '' };

    constructor(
        private dialog: MdDialogRef<AddDialogComponent>,
        private socket: SocketService
    ) { }

    public addFolder() {
        switch (this.selectedAction) {
            case 0:
                this.dialog.close({ action: 'mount volume', details: this.mountFolder });
                break;

            case 1:
                this.dialog.close({ action: 'add volume', details: this.folder });
                break;

            case 2:
                this.dialog.close({ action: 'download', details: this.downloadDetails });
                break;

            default:
                this.dialog.close();
                break;
        }
    }

    public cancel() {
        this.dialog.close();
    }

}
