import { Component, OnInit } from '@angular/core';
import { SettingsService } from '../settings-service/settings.service';
import { ISettings, Settings } from '../models/settings';

@Component({
    selector: 'app-settings',
    templateUrl: './settings.component.html',
    styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {

    public settings: ISettings = new Settings();

    constructor(private settingsService: SettingsService) { }

    /**
     * implamentation of the ngOnInit method, of the OnInit base class
     */
    ngOnInit() {
        this.settings = this.settingsService.get();

        // subscribe to the settings servive inorder to handle any changes
        this.settingsService.subscribe(newSettings => {
            this.settings = newSettings;
        });
    }

    /**
     * updates the new changes on the settings service
     */
    public onChange() {
        this.settingsService.set(this.settings);
    }

}
