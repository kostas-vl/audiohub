/* Fundamental Libraries */
import { BrowserModule, HammerGestureConfig, HAMMER_GESTURE_CONFIG } from '@angular/platform-browser';
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

/* Audiohub services */
import { SettingsService } from './settings-service/settings.service';
import { PageLoaderService } from './page-loader-service/page-loader.service';
import { SocketService } from './socket/socket.service';

/* Audiohub components */
import { AppComponent } from './app.component';
import { LoaderComponent } from './loader/loader.component';
import { PlayerComponent } from './player/player.component';
import { PlaylistComponent } from './playlist/playlist.component';
import { FilesComponent } from './files/files.component';
import { TopBarComponent } from './top-bar/top-bar.component';
import { StreamComponent } from './stream/stream.component';
import { SettingsComponent } from './settings/settings.component';
import { DownloadComponent } from './download/download.component';
import { SystemsComponent } from './systems/systems.component';
import { PageLoaderComponent } from './page-loader/page-loader.component';
import { OverlayContainer } from '@angular/cdk/overlay';

const appRoutes: Routes = [
    {
        path: 'playlist',
        component: PlaylistComponent
    },
    {
        path: 'files',
        component: FilesComponent
    },
    {
        path: 'stream',
        component: StreamComponent
    },
    {
        path: 'systems',
        component: SystemsComponent
    },
    {
        path: 'download',
        component: DownloadComponent
    },
    {
        path: 'settings',
        component: SettingsComponent
    },
    {
        path: '',
        redirectTo: '/playlist',
        pathMatch: 'full'
    },
    {
        path: '**',
        redirectTo: '/playlist',
        pathMatch: 'full'
    }
];

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
        RouterModule.forRoot(appRoutes),
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
        MatSidenavModule
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
