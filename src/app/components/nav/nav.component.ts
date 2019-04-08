import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnInit {
  navShow = false
  constructor() { }

  ngOnInit() {
  }

  toggleNav(){
    this.navShow = !this.navShow;
  }
}
