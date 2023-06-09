import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AppService } from 'src/app/shared/services/app.service';

@Component({
  selector: 'app-buy-token',
  templateUrl: './buy-token.component.html',
  styleUrls: ['./buy-token.component.scss']
})
export class BuyTokenComponent implements OnInit {


  tokensToBuy: number[];
  tokenList: number[];

  constructor(private appService: AppService,
    public dialogRef: MatDialogRef<BuyTokenComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {tokenList: number[]}) {

    this.tokensToBuy = [0, 0, 0, 0, 0, 0];
    this.tokenList = data.tokenList;
  }

  ngOnInit(): void {
  }

  buyToken(i: number) : void {
    if (this.tokenList[i] > this.tokensToBuy[i]) {
      ++this.tokensToBuy[i];
    }
  }

  cancelToken(i: number) : void {
    if (this.tokensToBuy[i] > 0) {
      --this.tokensToBuy[i];
    }
  }

  buyTokensConfirmation(): void {
    this.appService.buyTokens(this.tokensToBuy);
    this.dialogRef.close();
  }



}
