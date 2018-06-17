import { Component } from '@angular/core';
import { HttpService } from './Services/http.service';




@Component({
  selector: 'app-root',
  templateUrl: '../assets/html/app.component.html',
  styleUrls: ['../assets/scss/app.component.scss']
})

export class AppComponent {

  public candidate_list;

  constructor(private http: HttpService
  ) {
    const res = this.http.get_candidate_list().subscribe(resp => {
      this.candidate_list = resp;
      console.log(resp);
      let strLength = 3;
      strLength = 1;
      strLength = 2;
      console.log(strLength);

    });
  }


  list1: [string, number];
  test = [123, 'asd'];
  title = 'app';
  list = [1, 2 , 3, 4];
  count = 100;

  test1() {
    this.list1 = ['1', 1];

    const someValue: any = 1;
    // tslint:disable-next-line:prefer-const
    let strLength: number;
    strLength = 1;
    strLength = 2;
    console.log(strLength);
  }


}
