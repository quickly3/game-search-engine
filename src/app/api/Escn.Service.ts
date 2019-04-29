import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class EscnService {
    constructor(private http: HttpClient) { }

    getWordsCloud = params => {
        return this.http.get('/escn/getWordsCloud', { params });
    }

    searchDatasSimple = params => {
        return this.http.get('/escn/getDailyList', { params });
    }

    getDailyList = params => {
        return this.http.get('/escn/getDailyList', { params });
    }

    

}

