import { Component, OnInit } from '@angular/core';
import { MdDialogRef } from '@angular/material';
import { SocketService } from 'app/socket/socket.service';

class MountFolder {

  public ip = '';
  public volume = '';
  public user = '';
  public password = '';

}

@Component({
  selector: 'app-add-folder-dialog',
  templateUrl: './add-folder-dialog.component.html',
  styleUrls: ['./add-folder-dialog.component.css']
})
export class AddFolderDialogComponent {

  public addOptions = [
    { label: 'Mount Network Folder', value: 0 },
    { label: 'Add Local Folder', value: 1 }
  ];

  public selectedAction = 0;

  public mountFolder = new MountFolder();

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
        break;

      default:
        break;
    }
    this.dialog.close();
  }

  public cancel() {
    this.dialog.close();
  }

}
