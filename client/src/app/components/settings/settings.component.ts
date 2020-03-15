import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { ISettings, Settings } from 'src/app/models/settings';
import { SettingsService } from 'src/app/services/settings/settings.service';

@Component({
    selector: 'app-settings',
    templateUrl: './settings.component.html',
    styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit, OnDestroy {

    private onSettingsChangedSub?: Subscription;

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
        this.onSettingsChangedSub = this
            .settingsService
            .onSettingsChanged
            .subscribe(newSettings => this.settings = newSettings);
    }

    /**
     * Implementation of the ngOnDestroy method, of the OnDestroy base class
     * @memberof SettingsComponent
     */
    public ngOnDestroy() {
        this.onSettingsChangedSub?.unsubscribe();
    }

    /**
     * Updates the new changes on the settings service
     * @memberof SettingsComponent
     */
    public onChange() {
        this.settingsService.change(this.settings);
    }

}
