import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';



@Component({
    selector: 'games',
    templateUrl: '/assets/html/games.component.html',
    styleUrls: ['/assets/scss/games.component.scss']
})


export class GamesComponent {
    game_list
    total_number = 70;
    current_page = 1
    row = 20;

    constructor(private http: HttpClient) {
        this.getGameDatas();
    }

    configUrl = '/game/list';

    getGameDatas() {

        this.http.get('/game/list', { params: { page: "" + this.current_page } }).subscribe((data) => {
            this.game_list = data['data'];

            this.game_list = this.game_list.map((item) => {
                item.game_tags = item.game_tags_string;
                return item;
            })
            this.total_number = data['total'];
            console.log(this.total_number);
            console.log(this.current_page);


        });;
    }

    pageChange() {
        this.getGameDatas();
        console.log(this.current_page);
    }

    title = 'my-app';


}
