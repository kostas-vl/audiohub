import { Component, OnInit } from '@angular/core';
import { ITrack, TrackType } from '../track/track.model';
import { SocketService } from 'app/socket/socket.service';

@Component({
  selector: 'app-playlist',
  templateUrl: './playlist.component.html',
  styleUrls: ['./playlist.component.css']
})
export class PlaylistComponent implements OnInit {

  public playlist: ITrack[] = [];

  constructor(private socket: SocketService) { }

  public ngOnInit() {
    this.socket.subscribe('queue', data => this.playlist = data);
    this.socket.emit('queue');
  }

  public onPlaylist() {
    this.socket.emit('queue');
  }

}
