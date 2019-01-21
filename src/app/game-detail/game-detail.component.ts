import { Component, ViewEncapsulation } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { GameService } from 'app/api/gameService';
import { combineLatest } from 'rxjs';
import { debounceTime, distinctUntilChanged, map, switchMap, tap, catchError } from 'rxjs/operators';
import { Observable } from "rxjs"

@Component({
    selector: 'games',
    templateUrl: './game-detail.component.html',
    styleUrls: ['./game-detail.component.scss']
})

export class GameDetailComponent {
    gameService:any;
    game_id:string;
    game = {};

    constructor(
        private route: ActivatedRoute,
        gameService: GameService
    ){
        this.gameService = gameService;
        this.game_id = this.route.snapshot.paramMap.get("id");
    }

    ngOnInit() {
        this.gameService.getGameDataById({ id: this.game_id }).subscribe((data) => {
            this.game = data;
        });
    }

}
