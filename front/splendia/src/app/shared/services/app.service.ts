import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BoardState } from '../models/board_state.model';
import { BehaviorSubject, ReplaySubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class AppService {

  private _board_state = new ReplaySubject<BoardState>(1);
  constructor(private http: HttpClient) { }

  rootURL = 'http://127.0.0.1:5000/api';


  get board_state(){
    return this._board_state.asObservable();
  }

  launchGame() {
    this.http.get<BoardState>(this.rootURL + '/launch_game?nb_player=2')
    .subscribe(
      board_state =>{
        this._board_state.next(Object.assign({}, board_state));
      },
      error => console.log('Error while trying to launch game')
    );
  }

  // buyCard() {
  //   return this.http.get<BoardState>(this.rootURL + '/buy_card');
  // }

  takeToken() {
    this.http.get<BoardState>(this.rootURL + '/take_token')
    .subscribe(
      board_state =>{
        this._board_state.next(Object.assign({}, board_state));
      },
      error => console.log('Error while trying to take tokens')
    );
  }

  buyCard(cardId:number){
    this.http.get<BoardState>(this.rootURL + '/buy_card?card_id=' + cardId)
    .subscribe(
      board_state =>{
        this._board_state.next(Object.assign({}, board_state));
      },
      error => console.log('Error while trying to buy a card')
    );
  }

  reserveCard(cardId:number){
    this.http.get<BoardState>(this.rootURL + '/reserve_card?cardId=' + cardId)
    .subscribe(
      board_state =>{
        this._board_state.next(Object.assign({}, board_state));
      },
      error => console.log('Error while trying to reserve a card')
    );
  }

  buyTokens(tokensToBuy:number[]){
    this.http.get<BoardState>(this.rootURL + '/take_tokens?token_list=[' + tokensToBuy + ']')
    .subscribe(
      board_state =>{
        this._board_state.next(Object.assign({}, board_state));
      },
      error => console.log('Error while trying to buy tokens')
    );
  }
}
