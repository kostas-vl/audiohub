import { Injectable } from '@angular/core';
import { ISettings, Settings } from '../models/settings';

@Injectable()
export class SettingsService {

    private subscribers: Array<(settings: ISettings) => void> = [];
    private settings: ISettings = new Settings();

    constructor() { }

    public subscribe(callback: (settings: ISettings) => void) {
        this.subscribers.push(callback);
        return this.subscribers.length - 1;
    }

    public unsubscribe(index: number) {
        this.subscribers.splice(index, 1);
    }

    public get() {
        return this.settings;
    }

    public set(settings: ISettings) {
        this.settings = settings;
        for (const callback of this.subscribers) {
            callback(this.settings);
        }
    }

}
