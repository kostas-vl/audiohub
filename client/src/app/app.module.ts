/* Fundamental Libraries */
import { BrowserModule, HammerGestureConfig } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { OverlayContainer } from '@angular/cdk/overlay';
import { AppRoutingModule } from 'src/app/app.routing';

/* Audiohub services */
import { SettingsService } from 'src/app/services/settings/settings.service';
import { PageLoaderService } from 'src/app/services/page-loader/page-loader.service';
import { SocketService } from 'src/app/services/socket/socket.service';

/* Audiohub components */
import { AppComponent } from 'src/app/components/root/app.component';
import { LoaderComponent } from 'src/app/components/loader/loader.component';
import { PlayerComponent } from 'src/app/components/player/player.component';
import { PlaylistComponent } from 'src/app/components/playlist/playlist.component';
import { FilesComponent } from 'src/app/components/files/files.component';
import { TopBarComponent } from 'src/app/components/top-bar/top-bar.component';
import { StreamComponent } from 'src/app/components/stream/stream.component';
import { SettingsComponent } from 'src/app/components/settings/settings.component';
import { DownloadComponent } from 'src/app/components/download/download.component';
import { SystemsComponent } from 'src/app/components/systems/systems.component';
import { PageLoaderComponent } from 'src/app/components/page-loader/page-loader.component';


@NgModule({
    declarations: [
        AppComponent,
        LoaderComponent,
        TopBarComponent,
        PlayerComponent,
        PlaylistComponent,
        FilesComponent,
        StreamComponent,
        SettingsComponent,
        DownloadComponent,
        SystemsComponent,
        PageLoaderComponent,
    ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        MatIconModule,
        MatTooltipModule,
        MatButtonModule,
        MatInputModule,
        MatSelectModule,
        MatCheckboxModule,
        MatSlideToggleModule,
        MatSliderModule,
        MatProgressSpinnerModule,
        MatProgressBarModule,
        MatSnackBarModule,
        MatTabsModule,
        MatListModule,
        MatToolbarModule,
        MatCardModule,
        MatSidenavModule,
        AppRoutingModule
    ],
    entryComponents: [],
    providers: [
        SettingsService,
        PageLoaderService,
        SocketService
    ],
    bootstrap: [
        AppComponent
    ]
})
export class AppModule {

    constructor(private overlayContainer: OverlayContainer) {
        overlayContainer
            .getContainerElement()
            .classList
            .add('app-light');
    }

}
