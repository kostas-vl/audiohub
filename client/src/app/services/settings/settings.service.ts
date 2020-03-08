import { Injectable } from '@angular/core';
import { ISettings, Settings } from '../models/settings';
import { SocketService } from '../socket/socket.service';

type SettingsChangeEvent = (settings: ISettings) => void;

@Injectable()
export class SettingsService {

    private subscribers: SettingsChangeEvent[] = [];
    private settings: ISettings = new Settings();

    /**
     * Creates an instance of SettingsService.
     * @memberof SettingsService
     */
    constructor(private socket: SocketService) { }

    /**
     * Executes all the subscribed callbacks
     * @private
     * @memberof SettingsService
     */
    private broadcastChanges() {
        for (const callback of this.subscribers) {
            callback(this.settings);
        }
    }

    /**
     * Registers handlers for event messages from the server socket
     * @memberof SettingsService
     */
    public configure() {
        this.socket.subscribe('user settings', (data: ISettings) => {
            this.settings = data;
            this.broadcastChanges();
        });
    }

    /**
     * Add a callback to the subscriptions list, so that is executed when a change in settings occures
     * @param {(settings: ISettings) => void} callback to be executed when a change to the settings occurs
     * @returns the index of the new subscribption which is its identifier
     * @memberof SettingsService
     */
    public subscribe(callback: (settings: ISettings) => void) {
        this.subscribers.push(callback);
        return this.subscribers.length - 1;
    }

    /**
     * Remove a callback from the subscription list
     * @param {number} index of the callback on the list
     * @memberof SettingsService
     */
    public unsubscribe(index?: number) {
        if (index) {
            this.subscribers.splice(index, 1);
        }
    }

    /**
     * Return the current state of the settings
     * @returns the instance of the available settings
     * @memberof SettingsService
     */
    public get() {
        return this.settings;
    }

    /**
     * Set a state for the settigns an execute every callback on the subscription list
     * @param {ISettings} settings model to be assigned
     * @memberof SettingsService
     */
    public set(settings: ISettings) {
        this.settings = settings;
        this.broadcastChanges();
        this.socket.emit('user settings changed', this.settings);
    }

}
