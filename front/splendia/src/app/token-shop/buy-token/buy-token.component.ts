import { Component, OnInit } from '@angular/core';
import { AppService } from 'src/app/shared/services/app.service';

@Component({
  selector: 'app-buy-token',
  templateUrl: './buy-token.component.html',
  styleUrls: ['./buy-token.component.scss']
})
export class BuyTokenComponent implements OnInit {

  tokensToBuy: number[];

  constructor(private appService: AppService) {
    this.tokensToBuy = [0, 0, 0, 0, 0, 0];
  }

  ngOnInit(): void {
  }

  buyTokens(): void {
    this.appService.buyTokens(this.tokensToBuy);
  }

}
