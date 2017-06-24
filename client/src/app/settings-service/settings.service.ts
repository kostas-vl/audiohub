import { Injectable } from '@angular/core';
import { ISettings, Settings } from '../models/settings';

@Injectable()
export class SettingsService {

    private subscribers: Array<(settings: ISettings) => void> = [];
    private settings: ISettings = new Settings();

    constructor() { }

    /**
     * add a callback to the subscriptions list, so that is executed when a change in settings occures
     * @param callback to be executed
     */
    public subscribe(callback: (settings: ISettings) => void) {
        this.subscribers.push(callback);
        return this.subscribers.length - 1;
    }

    /**
     * remove a callback from the subscription list
     * @param index of the callback on the list
     */
    public unsubscribe(index: number) {
        this.subscribers.splice(index, 1);
    }

    /**
     * return the current state of the settings
     */
    public get() {
        return this.settings;
    }

    /**
     * set a state for the settigns an execute every callback on the subscription list
     * @param {ISettings} settings model to be assigned
     */
    public set(settings: ISettings) {
        this.settings = settings;
        for (const callback of this.subscribers) {
            callback(this.settings);
        }
    }

}
