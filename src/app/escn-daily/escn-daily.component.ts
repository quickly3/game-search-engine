import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';


import { Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, map, switchMap, tap, catchError } from 'rxjs/operators';
import { EscnService } from 'app/api/Escn.Service';


@Component({
    selector: 'escn-daily',
    templateUrl: './escn-daily.component.html',
    styleUrls: ['./escn-daily.component.scss']
})


export class EscnDailyComponent {
    escn_list = [];
    total_number = 0;
    current_page = 1;
    row = 10;

    keywords = "";

    words_cloud;
    escnService;

    search_by_keywords;

    constructor(
        private http: HttpClient,
        escnService: EscnService
    ) {
        this.escnService = escnService;
    }

    ngOnInit(): void {
        this.escnService.getWordsCloud().subscribe((words_cloud) => {
            this.words_cloud = words_cloud;
        });
        this.search();
    }

    searchKeyDown = function ($event) {
        this.search();
    }

    search = function () {
        let params = {
            page: "" + this.current_page,
            keywords: this.keywords
        };

        this.escnService.getDailyList(params).subscribe((data) => {
            this.escn_list = data['data'];
            // this.escn_list.map(item=>{item.unfold = false});
            this.total_number = data['total'];
        });
    }

    pageChange = () => { this.search(); }

    wordsCloudToKeyWords = function (word) {
        this.current_page = 0;
        this.keywords = word.key;
        this.search();
    }

    search_typeahead = (text$: Observable<string>) =>
        text$.pipe(
            debounceTime(300),
            tap(),
            switchMap(term =>
                this.searchDatasSimple(term).pipe(
                    tap(),
                    catchError(() => {
                        return of([]);
                    }))
            ),
        )

    searchDatasSimple = (term: any) => {
        let params = {
            page: "1",
            keywords: term,
            search_type: "simple"
        };
        return this.escnService.searchDatasSimple(params).pipe(
            map((response) => {
                let titles = response['data'].map((item => item.title));
                return titles;
            })
        );
    }

}
