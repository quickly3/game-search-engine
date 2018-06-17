import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpConfig } from '../Config/http';

@Injectable()

export class HttpService {
    constructor(private http: HttpClient, private urls: HttpConfig) {
    }

    get_candidate_list() {
        return this.http.get(this.urls.Home.get_candidate_list);
    }

}
