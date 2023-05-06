import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-token-shop',
  templateUrl: './token-shop.component.html',
  styleUrls: ['./token-shop.component.scss']
})
export class TokenShopComponent implements OnInit {

  tokenQuantities : number[] = [7,7,7,7,7,5];

  constructor() { }

  ngOnInit(): void {
  }

}
