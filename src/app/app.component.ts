import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: '../assets/html/app.component.html',
  styleUrls: ['../assets/scss/app.component.scss']
})

export class AppComponent {

  constructor(
    private http: HttpClient
  ) {
    // const res = this.http.get('/Home/list');
    // console.log(res);
  }

  title = 'app';
  list = [1, 2 , 3, 4];
  count = 100;
}
