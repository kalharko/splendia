import { AfterContentInit, Component, Input, OnInit } from '@angular/core';
import { BoardState } from 'src/app/shared/models/board_state.model';

@Component({
  selector: 'app-card-shop',
  templateUrl: './card-shop.component.html',
  styleUrls: ['./card-shop.component.scss']
})
export class CardShopComponent implements OnInit {

  board_state: BoardState;
  
  constructor() { }

  ngOnInit(): void {}


}
