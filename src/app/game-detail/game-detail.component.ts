import { Component, ViewEncapsulation } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { HttpClient } from '@angular/common/http';




@Component({
    selector: 'games',
    templateUrl: './game-detail.component.html',
    styleUrls: ['./game-detail.component.scss']
})




export class GameDetailComponent {

    ngOnInit(params: ParamMap) {
        console.log(params)
        console.log(123);
    }

}
