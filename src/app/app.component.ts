import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  game_list
  constructor(private http: HttpClient) { 
    var req = this.getConfig();
  
    req.subscribe((data) =>  {
      this.game_list = data['data'];
    });

  }

  configUrl = 'game/list';

  getConfig() {
    return this.http.get('game/list');
  }
  
  title = 'my-app';

  
}
