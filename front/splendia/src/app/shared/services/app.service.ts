import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BoardState } from '../models/board_state.model';

@Injectable({
  providedIn: 'root'
})

export class AppService {
  constructor(private http: HttpClient) { }

  rootURL = 'http://127.0.0.1:5000/api';

  takeToken() {
    return this.http.get<BoardState>(this.rootURL + '/takeToken');
  }

}
