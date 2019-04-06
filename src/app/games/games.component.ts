import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import {Observable,of} from 'rxjs';
import { debounceTime, distinctUntilChanged, map, switchMap, tap, catchError} from 'rxjs/operators';
import { GameService } from 'app/api/gameService';

@Component({
    selector: 'games',
    templateUrl: './games.component.html',
    styleUrls: ['./games.component.scss']
})


export class GamesComponent {
    game_list = [];
    total_number = 70;
    current_page = 1;
    row = 20;
    game_keywords = "";
    gameService

    constructor(
        private http: HttpClient,
        gameService: GameService
        
        ) { 
            this.gameService = gameService;

        }

    ngOnInit(): void {
        this.getGameDatas();
    }

    searchKeyDown = (event:any) => {
        if (event.key === "Enter") {
            this.getGameDatas();
        }
    }

    getGameDatas = () => {
        let params = { 
            page: "" + this.current_page,
            keywords: this.game_keywords
        };

        this.gameService.getGamesApi(params).subscribe((data) => {
            this.game_list = data['data'];
            this.total_number = data['total'];
        });
    }

    getGameDatasSimple = (term:any) => {
        let params = {
            page: "1",
            keywords: term,
            search_type:"simple"
        };
        return this.gameService.getGameDatasSimpleApi(params).pipe(
            map((response) => {
                let names = response['data'].map((item => item.name));
                return names;
            })
        );
    }

    pageChange = () => { this.getGameDatas(); }
    search = ()=>{
        this.getGameDatas();
    }
    // search_by_keywords = ()=>{}
    search_by_keywords  = (text$: Observable<string>) =>
        text$.pipe(
            debounceTime(300),
            tap(),
            switchMap(term =>
                this.getGameDatasSimple(term).pipe(
                    tap(),
                    catchError(() => {
                        return of([]);
                    }))
            ),
        )

    searchMore = ($event)=>{
        this.game_keywords = $event.item;
        this.search();
    }
}
