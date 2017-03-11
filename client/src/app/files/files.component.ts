import { Component, OnInit } from '@angular/core';
import { MdDialog } from '@angular/material';

import { FileSystemEntry } from 'app/files/file-system-entry/file-system-entry';
import { SocketService } from 'app/socket/socket.service';
import { AddFolderDialogComponent } from 'app/files/add-folder-dialog/add-folder-dialog.component';

@Component({
  selector: 'app-files',
  templateUrl: './files.component.html',
  styleUrls: ['./files.component.css']
})
export class FilesComponent implements OnInit {

  public systems: FileSystemEntry[] = [];

  public selectedSystem: FileSystemEntry;

  public currentSystem: FileSystemEntry;

  public currentSystemStack: string[] = [];

  constructor(
    private socket: SocketService,
    private mdDialog: MdDialog
  ) { }

  private currentPath() {
    return this.currentSystemStack[this.currentSystemStack.length - 1];
  }

  public ngOnInit() {
    this.socket.subscribe('available systems', data => {
      this.systems = data;
      this.currentSystem = this.systems[0];
      this.currentSystemStack = [this.currentSystem.path];
      this.socket.emit('list dir', this.currentPath());
    });

    this.socket.subscribe('list dir', data => this.currentSystem.entries = data);

    this.socket.subscribe('mount volume success', data => {
      this.systems.push(data);
      this.socket.emit('list dir', data.path);
    });

    this.socket.emit('available systems');
  }

  public entryClick(entry: FileSystemEntry) {
    if (entry.type === 'directory') {
      this.openDir(entry.path);
    }
  }

  public openDialog() {
    const dialog = this.mdDialog.open(AddFolderDialogComponent);
    dialog.afterClosed().subscribe(data => {
      if (data.action === 'mount') {
        this.socket.emit('mount volume', data.details);
      } else {

      }
    });
  }

  public homeDir() {
    this.currentSystemStack = [this.currentSystemStack[0]];
    this.socket.emit('list dir', this.currentPath());
  }

  public previousDir() {
    this.currentSystemStack.pop();
    this.socket.emit('list dir', this.currentPath());
  }

  public openDir(path) {
    this.socket.emit('list dir', path + '/');
    this.currentSystemStack.push(path);
  }

}
