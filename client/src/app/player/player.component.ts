import { Component, OnInit } from '@angular/core';
import { SocketService } from 'app/socket/socket.service';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit {

  public volume = 100;
  public playing = false;

  constructor(private socket: SocketService) { }

  ngOnInit() { }

  public onPlay() {
    this.socket.emit('play');
    this.playing = true;
  }

  public onPause() {
    this.socket.emit('pause');
    this.playing = false;
  }

  public onStop() {
    this.socket.emit('stop');
    this.playing = false;
  }

  public onVolume(value: number) {
    this.socket.emit('volume', value);
  }

}
