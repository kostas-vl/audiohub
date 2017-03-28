import { Component, OnInit } from '@angular/core';
import { MdDialog } from '@angular/material';

import { IFileSystem, FileSystem } from 'app/models/file-system';
import { SocketService } from 'app/socket/socket.service';
import { AddFolderDialogComponent } from 'app/files/add-folder-dialog/add-folder-dialog.component';

@Component({
  selector: 'app-files',
  templateUrl: './files.component.html',
  styleUrls: ['./files.component.css']
})
export class FilesComponent implements OnInit {

  public systems: IFileSystem[] = [];

  public selectedSystem: IFileSystem;

  public currentSystem: IFileSystem;

  public currentSystemEntries: IFileSystem[];

  public currentSystemStack: string[] = [];

  constructor(
    private socket: SocketService,
    private mdDialog: MdDialog
  ) { }

  private currentPath() {
    return this.currentSystemStack[this.currentSystemStack.length - 1];
  }

  public ngOnInit() {
    this.socket.subscribe('available systems', (data: IFileSystem[]) => {
      if (data) {
        this.systems = data;
        this.currentSystem = this.systems[0];
        this.currentSystemStack = [this.currentSystem.path];
        this.socket.emit('list dir', this.currentPath());
      }
    });

    this.socket.subscribe('list dir', (data: IFileSystem[]) => {
      this.currentSystemEntries = data;
    });

    this.socket.subscribe('mount volume success', (data: IFileSystem) => {
      this.systems.push(data);
      this.socket.emit('list dir', data.path);
    });

    this.socket.subscribe('add volume success', (data: IFileSystem) => {
      this.systems.push(data);
      this.socket.emit('list dir', data.path);
    });

    this.socket.emit('available systems');
  }

  public openDialog() {
    const dialog = this.mdDialog.open(AddFolderDialogComponent);
    dialog.afterClosed().subscribe(data => {
      if (data && data.action === 'mount') {
        this.socket.emit('mount volume', data.details);
      } else if (data && data.action === 'add folder') {
        this.socket.emit('add volume', data.details);
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

  public entryClick(entry: IFileSystem) {
    if (entry.type === 'directory') {
      this.openDir(entry.path);
    }
  }

  public openDir(path: string) {
    this.socket.emit('list dir', path);
    this.currentSystemStack.push(path);
  }

  public addToPlaylist(entry: IFileSystem) {
    this.socket.emit('queue push', entry);
  }

}
