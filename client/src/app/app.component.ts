import { Component, Input, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
import { SocketService } from './socket/socket.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

  constructor(private socket: SocketService) { }

  public ngOnInit() {
    this.socket.connect();
    this.socket.subscribe('track time', (data) => console.log(data));
  }  

  public ngOnDestroy() {
    this.socket.disconnect();
  }

}
