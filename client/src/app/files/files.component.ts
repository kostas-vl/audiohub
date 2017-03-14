import { Component, OnInit } from '@angular/core';
import { MdDialog } from '@angular/material';

import { FileSystemEntry } from 'app/file-system-entry/file-system-entry';
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
      this.socket.emit('list dir', '\\\\192.168.1.72\\shared');
    });

    this.socket.emit('available systems');
  }

  public openDialog() {
    const dialog = this.mdDialog.open(AddFolderDialogComponent);
    dialog.afterClosed().subscribe(data => {
      if (data && data.action === 'mount') {
        this.socket.emit('mount volume', data.details);
      }
    });
  }

  public changeSystem(path: string) {
    const entry = this.systems.find(f => f.path === path);
    if (entry) {
      this.currentSystem = entry;
      this.currentSystemStack = [];
      this.openDir(entry.path);
    }
  }

  public homeDir() {
    this.currentSystemStack = [this.currentSystemStack[0]];
    this.socket.emit('list dir', this.currentPath());
  }

  public previousDir() {
    this.currentSystemStack.pop();
    this.socket.emit('list dir', this.currentPath());
  }

  public entryClick(entry: FileSystemEntry) {
    if (entry.type === 'directory') {
      this.openDir(entry.path);
    }
  }

  public openDir(path: string) {
    this.socket.emit('list dir', path);
    this.currentSystemStack.push(path);
  }

  public addToPlaylist(entry: FileSystemEntry) {
    this.socket.emit('queue push', entry);
  }

}
