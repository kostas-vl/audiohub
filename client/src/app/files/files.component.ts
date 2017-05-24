import { Component, OnInit } from '@angular/core';
import { MdDialog } from '@angular/material';

import { IFileSystem, FileSystem } from '../models/file-system';
import { SocketService } from '../socket/socket.service';
import { AddDialogComponent } from './add-dialog/add-dialog.component';

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
    public loading = false;
    public asyncLoading = false;

    constructor(
        private socket: SocketService,
        private mdDialog: MdDialog
    ) { }

    private availableSystems() {
        this.loading = true;
        this.socket.emit('available systems');
        this.socket.subscribe('available systems', (data: IFileSystem[]) => {
            if (data) {
                this.systems = data;
                this.currentSystem = this.systems[0];
                this.currentSystemEntries = this.systems;
                this.currentSystemStack = [];
                this.socket.emit('list dir', this.currentPath());
                this.loading = false;
            }
        });
    }

    private currentPath() {
        return this.currentSystemStack[this.currentSystemStack.length - 1];
    }

    private openDir(path: string) {
        this.loading = true;
        this.socket.emit('list dir', path);
        this.currentSystemStack.push(path);
    }

    public ngOnInit() {
        this.socket.subscribe('list dir', (data: IFileSystem[]) => {
            this.currentSystemEntries = data;
            setTimeout(() => this.loading = false, 500);
        });

        this.socket.subscribe('mount volume success', (data: IFileSystem) => {
            this.systems.push(data);
            this.socket.emit('list dir', data.path);
        });

        this.socket.subscribe('add volume success', (data: IFileSystem) => {
            this.systems.push(data);
            this.socket.emit('list dir', data.path);
        });

        this.socket.subscribe('download finished', _ => {
            this.asyncLoading = false;
        });

        this.availableSystems();
    }

    public onOpenDialog() {
        const dialog = this.mdDialog.open(AddDialogComponent);
        dialog.afterClosed().subscribe(data => {
            if (data) {
                this.asyncLoading = true;
                this.socket.emit(data.action, data.details);
            }
        });
    }

    public onRefresh() {
        this.socket.emit('list dir', this.currentPath());
    }

    public onHome() {
        this.currentSystemEntries = this.systems;
        this.currentSystemStack = [];
    }

    public onPrevious() {
        this.currentSystemStack.pop();
        if (this.currentSystemStack.length === 0) {
            this.onHome();
        } else {
            this.socket.emit('list dir', this.currentPath());
        }
    }

    public onEntry(entry: IFileSystem) {
        if (entry.type === 'directory') {
            this.openDir(entry.path);
        }
    }

    public onSystemDisconect(entry: IFileSystem) {
        this.socket.emit('remove volume', entry.id);
    }

    public onAdd(entry: IFileSystem) {
        this.socket.emit('queue push', entry);
    }

}
