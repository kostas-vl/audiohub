import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
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

const routes: Routes = [
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
    imports: [
        RouterModule.forRoot(routes)
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule { }

