import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class GameService {
    constructor(private http: HttpClient) { }

    getGamesApi = params => {
        return this.http.get('/game/list', { params });
    }

    getGameDatasSimpleApi = params => {
        return this.http.get('/game/list', { params });
    }

    getGameDataById = params => {
        return this.http.get('/game/getGameDataById', { params });
    }


}

