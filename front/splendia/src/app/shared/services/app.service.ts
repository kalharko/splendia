import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BoardState } from '../models/board_state.model';

@Injectable({
  providedIn: 'root'
})

export class AppService {
  constructor(private http: HttpClient) { }

  rootURL = 'http://127.0.0.1:5000/api';

  launchGame() {
    return this.http.get<BoardState>(this.rootURL + '/launch_game?nb_player=2');
  }

  // buyCard() {
  //   return this.http.get<BoardState>(this.rootURL + '/buy_card');
  // }

  takeToken() {
    return this.http.get<BoardState>(this.rootURL + '/take_tokens');
  }

}
