import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import {Observable,of} from 'rxjs';
import { debounceTime, distinctUntilChanged, map, switchMap, tap, catchError} from 'rxjs/operators';

const states = ['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado',
  'Connecticut', 'Delaware', 'District Of Columbia', 'Federated States Of Micronesia', 'Florida', 'Georgia',
  'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
  'Marshall Islands', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
  'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
  'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico', 'Rhode Island',
  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia',
  'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'];


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

    constructor(private http: HttpClient) {
        this.getGameDatas();
    }

    configUrl = '/game/list';

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
        this.http.get('/game/list', { params }).subscribe((data) => {
            this.game_list = data['data'];

            this.game_list = this.game_list.map((item) => {
                item.game_tags = item.game_tags_string;
                return item;
            });
            this.total_number = data['total'];
        });
    }

    getGameDatasSimple = (term) => {
        let params = {
            page: "1",
            keywords: term,
            search_type:"simple"
        };
        return this.http.get('/game/list', { params }).pipe(
            map( (response)=> {  
                let names = response['data'].map((item=>item.name));
                return names; 
            })
        );
    }

    pageChange = () => {
        this.getGameDatas(); 
    }

    title = 'my-app';
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
}
