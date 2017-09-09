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

    /**
     * Creates an instance of SettingsComponent.
     * @memberof SettingsComponent
     */
    constructor(private settingsService: SettingsService) { }

    /**
     * Implamentation of the ngOnInit method, of the OnInit base class
     * @memberof SettingsComponent
     */
    public ngOnInit() {
        this.settings = this.settingsService.get();

        // subscribe to the settings servive inorder to handle any changes
        this.settingsService.subscribe(newSettings => {
            this.settings = newSettings;
        });
    }

    /**
     * Updates the new changes on the settings service
     * @memberof SettingsComponent
     */
    public onChange() {
        this.settingsService.set(this.settings);
    }

}
