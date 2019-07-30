import { Component, OnInit } from '@angular/core';

import { Observable, of } from 'rxjs';
import { scan } from 'rxjs/operators';
import { debounceTime, distinctUntilChanged, map, switchMap, tap, catchError } from 'rxjs/operators';
import { FanjuService } from 'app/api/fanju.service';

import { fromEvent } from 'rxjs';

@Component({
  selector: 'app-fanju',
  templateUrl: './fanju.component.html',
  styleUrls: ['./fanju.component.scss']
})
export class FanjuComponent implements OnInit {

  fanju_list = [];
  total_number = 0;
  current_page = 1;
  row = 10;
  game_keywords = "";
  fanjuService

  constructor(fanjuService: FanjuService) {
    this.fanjuService = fanjuService
  }

  ngOnInit() {

    fromEvent(document, 'click')
      .pipe(scan(count => count + 1, 0))
      .subscribe(count => console.log(`Clicked ${count} times`));

    this.getFanjuDatas();
  }

  searchKeyDown = (event: any) => {
    if (event.key === "Enter") {
      this.getFanjuDatas();
    }
  }

  // search_by_keywords = (text$: Observable<string>) =>
  //   text$.pipe(
  //     debounceTime(300),
  //     tap(),
  //     switchMap(term =>
  //       this.getGameDatasSimple(term).pipe(
  //         tap(),
  //         catchError(() => {
  //           return of([]);
  //         }))
  //     ),
  //   )

  pageChange = () => { this.getFanjuDatas(); }

  search_by_keywords = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(300),
      tap(),
      switchMap(term =>
        this.getFanjuDatasSimple(term).pipe(
          tap(),
          catchError(() => {
            return of([]);
          }))
      ),
    )


  searchMore = ($event) => {

  }

  search = () => {
    this.getFanjuDatas();
  }

  getFanjuDatasSimple = (term: any) => {
    let params = {
      page: "1",
      keywords: term,
      search_type: "simple"
    };
    return this.fanjuService.getFanjuDatasSimpleApi(params).pipe(
      map((response) => {
        let names = response['data'].map((item => item.name));
        return names;
      })
    );
  }

  getFanjuDatas() {
    let params = {
      page: "" + this.current_page,
      keywords: this.game_keywords
    };

    this.fanjuService.getFanjuApi(params).subscribe((data) => {
      this.fanju_list = data['data'];
      this.fanju_list.map(item => { item.unfold = false });
      this.total_number = data['total'];
    });
  }

}
