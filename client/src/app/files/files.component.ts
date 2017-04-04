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
            // this.loading = false;
        });

        this.socket.subscribe('mount volume success', (data: IFileSystem) => {
            this.systems.push(data);
            this.socket.emit('list dir', data.path);
        });

        this.socket.subscribe('add volume success', (data: IFileSystem) => {
            this.systems.push(data);
            this.socket.emit('list dir', data.path);
        });

        this.availableSystems();
    }

    public onOpenDialog() {
        const dialog = this.mdDialog.open(AddDialogComponent);
        dialog.afterClosed().subscribe(data => {
            if (data) {
                this.socket.emit(data.action, data.details);
            }
        });
    }

    public onRefresh() {
        this.availableSystems();
    }

    public onHome() {
        this.currentSystemEntries = this.systems;
        this.currentSystemStack = [];
    }

    public onPrevious() {
        this.currentSystemStack.pop();
        this.socket.emit('list dir', this.currentPath());
    }

    public onEntry(entry: IFileSystem) {
        if (entry.type === 'directory') {
            this.openDir(entry.path);
        }
    }

    public onAdd(entry: IFileSystem) {
        this.socket.emit('queue push', entry);
    }

}
