import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class FanjuService {
    constructor(private http: HttpClient) { }

    getFanjuApi = params => {
        return this.http.get('/fanju/list', { params });
    }

    getFanjuDatasSimpleApi = params => {
        return this.http.get('/fanju/list', { params });
    }

    // getGameDataById = params => {
    //     return this.http.get('/fanju/getGameDataById', { params });
    // }

}

