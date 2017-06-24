import { Component, OnInit, ViewChild, Output, EventEmitter } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MdTabGroup } from '@angular/material';
import { SocketService } from '../socket/socket.service';
import { IMountFolder, MountFolder } from '../models/mount-folder';
import { ILocalFolder, LocalFolder } from '../models/local-folder';
import { IDownloadDetails, DownloadDetails } from '../models/download-details';

@Component({
    selector: 'app-add-dialog',
    templateUrl: './add-dialog.component.html',
    styleUrls: ['./add-dialog.component.css']
})
export class AddDialogComponent {

    @Output()
    public complete: EventEmitter<{ action: string, details: any }> = new EventEmitter();
    @ViewChild(MdTabGroup)
    public tabGroupComponent: MdTabGroup;
    public mountFolder: IMountFolder = new MountFolder();
    public folder: ILocalFolder = new LocalFolder();
    public downloadDetails: IDownloadDetails = new DownloadDetails();
    public systemsControl: FormControl;
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
    public fileFormatOptions = [
        'mp3',
        'mp4',
        'wav'
    ];

    constructor(private socket: SocketService) { }

    /**
     * sends the appropriate event message, based on the currently edited, by the user, tab
     */
    public onComplete() {
        switch (this.tabGroupComponent.selectedIndex) {
            case 0:
                this.complete.emit({ action: 'mount volume', details: this.mountFolder });
                break;

            case 1:
                this.complete.emit({ action: 'add volume', details: this.folder });
                break;

            case 2:
                this.complete.emit({ action: 'download', details: this.downloadDetails });
                break;

            default:
                break;
        }
    }

}
