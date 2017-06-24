import { Component, OnInit } from '@angular/core';
import { MdSnackBar } from '@angular/material';
import { IFileSystem, FileSystem } from '../models/file-system';
import { SocketService } from '../socket/socket.service';

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
        private mdSnackBar: MdSnackBar
    ) { }

    /**
     * lists the contents of the directory on the provided path, and pushes the path on the
     * current stack
     * @param {string} path to the desired directory
     */
    private openDir(path: string) {
        this.loading = true;
        this.socket.emit('list dir', path);
        this.currentSystemStack.push(path);
    }

    /**
     * implementation on the ngOnInit method, of the OnInit base class
     */
    public ngOnInit() {
        // displays the loader
        this.loading = true;

        // subscribes an event handler for the 'available systems' event
        this.socket.subscribe('available systems', (data: IFileSystem[]) => {3
            this.systems = data;
            this.currentSystemEntries = this.systems;
            this.currentSystemStack = [];
            this.loading = false;
            setTimeout(() => this.loading = false, 500);
        });

        // subscribes an event handler for the 'list dir' event
        this.socket.subscribe('list dir', (data: IFileSystem[]) => {
            this.currentSystemEntries = data;
            setTimeout(() => this.loading = false, 500);
        });

        // subscribes an event handler for the 'mount volume success' event
        this.socket.subscribe('mount volume success', (data: IFileSystem) => {
            this.systems.push(data);
        });

        // subscribes an event handler for the 'add volume success' event
        this.socket.subscribe('add volume success', (data: IFileSystem) => {
            this.systems.push(data);
            if (this.currentSystemStack.length === 0) {
                this.onHome();
            }
        });

        // send an event message for the list of the available file systems
        this.socket.emit('available systems');
    }

    /**
     * refreshes the displyed list of entries
     */
    public onRefresh() {
        this.loading = true;
        if (this.currentSystemStack.length === 0) {
            this.socket.emit('available systems');
        } else {
            this.socket.emit('list dir', this.currentSystemStack[this.currentSystemStack.length - 1]);
        }
    }

    /**
     * immediately displays the available file systems
     */
    public onHome() {
        this.currentSystemEntries = this.systems;
        this.currentSystemStack = [];
    }

    /**
     * displays the files/directories, of the previous entry in the current stack
     */
    public onPrevious() {
        this.currentSystemStack.pop();
        if (this.currentSystemStack.length === 0) {
            this.onHome();
        } else {
            this.loading = true;
            this.socket.emit('list dir', this.currentSystemStack[this.currentSystemStack.length - 1]);
        }
    }

    /**
     * displays the contents on the provided file system, if it's a directory
     * @param {IFileSystem} entry of the currently displayed directory contents
     */
    public onEntry(entry: IFileSystem) {
        if (entry.type === 'directory') {
            this.openDir(entry.path);
        }
    }

    /**
     * sends a 'remove volume' event message, for the removal of base file system
     * @param {IFileSystem} entry of the list of base file systems
     */
    public onDisconect(entry: IFileSystem) {
        this.socket.emit('remove volume', entry.identity);
    }

    /**
     * sends a 'queue push' event message, for the addition of a file system on the list
     * of base file systems
     * @param {IFileSystem} newEntry for the list of base file systems 
     */
    public onAdd(newEntry: IFileSystem) {
        this.socket.emit('queue push', newEntry);
        this.mdSnackBar.open('Added: ' + newEntry.name, '', { duration: 1500 });
    }

}
