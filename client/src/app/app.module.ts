/* Fundamental Libraries */
import { BrowserModule, HammerGestureConfig, HAMMER_GESTURE_CONFIG } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { Routes, RouterModule } from '@angular/router';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { MaterialModule } from '@angular/material';
import { Ng2BootstrapModule } from 'ngx-bootstrap';

/* Audiohub services */
import { SocketService } from './socket/socket.service';

/* Audiohub components */
import { AppComponent } from './app.component';
import { LoaderComponent } from './loader/loader.component';
import { PlayerComponent } from './player/player.component';
import { PlaylistComponent } from './playlist/playlist.component';
import { FilesComponent } from './files/files.component';
import { AddDialogComponent } from './files/add-dialog/add-dialog.component';
import { TopBarComponent } from './top-bar/top-bar.component';
import { StreamComponent } from './stream/stream.component';
import { SettingsComponent } from './settings/settings.component';
import { SettingsService } from './settings-service/settings.service';

export class HammerJsConfiguration extends HammerGestureConfig {

    public override = {
        'swipe': {
            velocity: 0.4,
            threshold: 20
        }
    };

}

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
        AddDialogComponent,
        FilesComponent,
        StreamComponent,
        SettingsComponent,
    ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        HttpModule,
        MaterialModule,
        RouterModule.forRoot(appRoutes),
        Ng2BootstrapModule.forRoot()
    ],
    entryComponents: [
        AddDialogComponent
    ],
    providers: [
        SettingsService,
        SocketService,
        {
            provide: HAMMER_GESTURE_CONFIG,
            useClass: HammerJsConfiguration
        }
    ],
    bootstrap: [
        AppComponent
    ]
})
export class AppModule { }
