import { Component, OnInit, OnDestroy } from '@angular/core';
import { MdSnackBar } from '@angular/material';
import { IFileSystem, FileSystem } from '../models/file-system';
import { SocketService } from '../socket/socket.service';

@Component({
    selector: 'app-files',
    templateUrl: './files.component.html',
    styleUrls: ['./files.component.scss']
})
export class FilesComponent implements OnInit, OnDestroy {

    public systems: IFileSystem[] = [];
    public selectedSystem: IFileSystem;
    public currentSystem: IFileSystem;
    public currentSystemEntries: IFileSystem[] = [];
    public currentSystemStack: string[] = [];
    public loading = false;
    public asyncLoading = false;

    /**
     * Creates an instance of FilesComponent.
     * @memberof FilesComponent
     */
    constructor(
        private socket: SocketService,
        private mdSnackBar: MdSnackBar
    ) { }

    /**
     * Lists the contents of the directory on the provided path, and pushes the path on the
     * current stack
     * @private
     * @param {string} path to the desired directory
     * @memberof FilesComponent
     */
    private openDir(path: string) {
        this.loading = true;
        this.socket.emit('list dir', path);
        this.currentSystemStack.push(path);
    }

    /**
     * Holds an arrow function that handles the available systems event
     * @private
     * @param {IFileSystem[]} data for all the file systems
     * @memberof FilesComponent
     */
    private onAvailableSystems = (data: IFileSystem[]) => {
        this.systems = data;
        this.currentSystemEntries = this.systems;
        this.currentSystemStack = [];
        this.loading = false;
        setTimeout(() => {
            this.loading = false;
        }, 500);
    }

    /**
     * Hodls an arrow function that handles the list dir event
     * @private
     * @param {IFileSystem[]} data for the contents of the target directory
     * @memberof FilesComponent
     */
    private onListDir = (data: IFileSystem[]) => {
        this.currentSystemEntries = data;
        setTimeout(() => {
            this.loading = false;
        }, 500);
    }

    /**
     * Holds an arrow function that handles the mount volume success event
     * @private
     * @param {IFileSystem} data of the mounted volume
     * @memberof FilesComponent
     */
    private onMountVolumeSuccess = (data: IFileSystem) => {
        this.systems.push(data);
    }

    /**
     * Holds an arrow function that handles the add volume success event
     * @private
     * @param {IFileSystem} data for the added volume
     * @memberof FilesComponent
     */
    private onAddVolumeSuccess = (data: IFileSystem) => {
        this.systems.push(data);
        if (this.currentSystemStack.length === 0) {
            this.onHome();
        }
    }

    /**
     * Implementation on the ngOnInit method, of the OnInit base class
     * @memberof FilesComponent
     */
    public ngOnInit() {
        // displays the loader
        this.loading = true;

        this.socket
            .subscribe('available systems', this.onAvailableSystems);

        this.socket
            .subscribe('list dir', this.onListDir);

        this.socket
            .subscribe('mount volume success', this.onMountVolumeSuccess);

        this.socket
            .subscribe('add volume success', this.onAddVolumeSuccess);

        // send an event message for the list of the available file systems
        this.socket
            .emit('available systems');
    }

    /**
     * Implementation of the ngOnDestroy method, of the OnDestroy base class
     * @memberof FilesComponent
     */
    public ngOnDestroy() {
        // Unsubscribe from all the message event handlers
        this.socket
            .unsubscribe('available systems', this.onAvailableSystems);

        this.socket
            .unsubscribe('list dir', this.onListDir);

        this.socket
            .unsubscribe('mount volume success', this.onMountVolumeSuccess);

        this.socket
            .unsubscribe('add volume success', this.onAddVolumeSuccess);
    }

    /**
     * Refreshes the displyed list of entries
     * @memberof FilesComponent
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
     * Immediately displays the available file systems
     * @memberof FilesComponent
     */
    public onHome() {
        this.currentSystemEntries = this.systems;
        this.currentSystemStack = [];
    }

    /**
     * Displays the files/directories, of the previous entry in the current stack
     * @memberof FilesComponent
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
     * Displays the contents on the provided file system, if it's a directory
     * @param {IFileSystem} entry of the currently displayed directory contents
     * @memberof FilesComponent
     */
    public onEntry(entry: IFileSystem) {
        if (entry.type === 'directory') {
            this.openDir(entry.path);
        }
    }

    /**
     * Sends a 'remove volume' event message, for the removal of base file system
     * @param {IFileSystem} entry of the list of base file systems
     * @memberof FilesComponent
     */
    public onDisconect(entry: IFileSystem) {
        this.socket.emit('remove volume', entry.identity);
    }

    /**
     * Sends a 'queue push' event message, for the addition of a file system on the list
     * of base file systems
     * @param {IFileSystem} newEntry for the list of base file systems
     * @memberof FilesComponent
     */
    public onAdd(newEntry: IFileSystem) {
        this.socket.emit('queue push', newEntry);
        this.mdSnackBar.open('Added: ' + newEntry.name, '', { duration: 1500 });
    }

}
