import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})


export class AppComponent {
  game_list
  constructor(private http: HttpClient) { 
    var req = this.getConfig();
  
    req.subscribe((data) =>  {


      this.game_list = data['data'];

      this.game_list = this.game_list.map((item)=>{
        item.game_tags = item.game_tags_string.split(",")
        return item;
      })
      console.log(this.game_list);
    });

  }

  configUrl = 'game/list';

  getConfig() {
    return this.http.get('game/list');
  }
  
  title = 'my-app';

  
}
