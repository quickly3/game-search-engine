import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnInit {
  navShow = false
  constructor(public router: Router) {
    this.router = router;
  }

  ngOnInit() {
    // console.log(this.router);
    // this.router.url.then()
    // this.router.url.subscribe(url => console.log(url[0].path));
  }

  toggleNav() {
    this.navShow = !this.navShow;
  }
}
