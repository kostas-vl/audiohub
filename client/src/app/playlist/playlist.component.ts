import { Component, OnInit } from '@angular/core';
import { SocketService } from 'app/socket/socket.service';

import { FileSystemEntry } from 'app/file-system-entry/file-system-entry';

@Component({
  selector: 'app-playlist',
  templateUrl: './playlist.component.html',
  styleUrls: ['./playlist.component.css']
})
export class PlaylistComponent implements OnInit {

  public playlist: FileSystemEntry[] = [];

  constructor(private socket: SocketService) { }

  public ngOnInit() {
    this.socket.subscribe('queue', data => this.playlist = data);
    this.socket.emit('queue');
  }

  public onPlaylist() {
    this.socket.emit('queue');
  }

  public onPlayNow(entry: FileSystemEntry) {
    this.socket.emit('play now', entry);
  }

}
