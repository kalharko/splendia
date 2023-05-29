import { Component, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { AppService } from 'src/app/shared/services/app.service';
import {MatDialog} from '@angular/material/dialog';
import { RejectTokenComponent } from '../reject-token/reject-token.component';
import { BuyTokenComponent } from '../buy-token/buy-token.component';

@Component({
  selector: 'app-token-shop',
  templateUrl: './token-shop.component.html',
  styleUrls: ['./token-shop.component.scss']
})
export class TokenShopComponent extends OnDestroyMixin implements OnInit {

  // token quantities to display
  tokenList: number[] = [0, 0,0,0,0,0];

  constructor(private appService: AppService, public dialog: MatDialog) { 
    super();
  }

  ngOnInit(): void {
    // Subscribe to board_state.bank
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.tokenList = board_state.bank;
    });
  }

  takeToken(): void{
    let dialogRef = this.dialog.open(BuyTokenComponent, {
      height: '400px',
      width: '600px',
      data: { tokenList: this.tokenList }
    }

    );
    
  }
}
