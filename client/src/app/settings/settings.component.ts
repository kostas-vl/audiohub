import { Component, OnInit } from '@angular/core';
import { SettingsService } from '../settings-service/settings.service';
import { ISettings } from '../models/settings';

@Component({
    selector: 'app-settings',
    templateUrl: './settings.component.html',
    styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

    public settings: ISettings;

    constructor(private settingsService: SettingsService) { }

    ngOnInit() {
        this.settings = this.settingsService.get();
    }

    public onChange() {
        this.settingsService.set(this.settings);
    }

}
