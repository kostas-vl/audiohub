import { Component, OnInit } from '@angular/core';
import { MdDialogRef } from '@angular/material';
import { SocketService } from 'app/socket/socket.service';
import { IMountFolder, MountFolder } from 'app/files/add-folder-dialog/models/mount-folder';

@Component({
  selector: 'app-add-folder-dialog',
  templateUrl: './add-folder-dialog.component.html',
  styleUrls: ['./add-folder-dialog.component.css']
})
export class AddFolderDialogComponent {

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

  public selectedAction = 0;

  public mountFolder: IMountFolder = new MountFolder();

  public folder = { name: '', path: '' };

  constructor(
    private dialog: MdDialogRef<AddFolderDialogComponent>,
    private socket: SocketService
  ) { }

  public addFolder() {
    switch (this.selectedAction) {
      case 0:
        this.dialog.close({ action: 'mount', details: this.mountFolder });
        break;

      case 1:
        this.dialog.close({ action: 'add folder', details: this.folder });
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
