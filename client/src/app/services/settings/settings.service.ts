import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ISettings, Settings } from 'src/app/models/settings';
import { SocketService } from 'src/app/services/socket/socket.service';

type SettingsChangeEvent = (settings: ISettings) => void;

@Injectable()
export class SettingsService {

    private onSettingsChangedSource = new BehaviorSubject<ISettings>(new Settings());

    public onSettingsChanged = this.onSettingsChangedSource.asObservable();

    /**
     * Creates an instance of SettingsService.
     * @memberof SettingsService
     */
    constructor(private socket: SocketService) { }

    /**
     * Registers handlers for event messages from the server socket
     * @memberof SettingsService
     */
    public configure() {
        this.socket.subscribe('user settings', (data: ISettings) => {
            if (data) {
                this.onSettingsChangedSource.next(data);
            }
        });
    }

    /**
     * Set a state for the settigns an execute every callback on the subscription list
     * @param {ISettings} settings model to be assigned
     * @memberof SettingsService
     */
    public change(settings: ISettings) {
        if (settings) {
            this.socket.emit('user settings changed', settings);
            this.onSettingsChangedSource.next(settings);
        }
    }

}
