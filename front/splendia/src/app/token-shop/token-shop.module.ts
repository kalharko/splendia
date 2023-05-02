import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TokenShopComponent } from './token-shop/token-shop.component';
import { RejectTokenComponent } from './reject-token/reject-token.component';
import { BuyTokenComponent } from './buy-token/buy-token.component';



@NgModule({
  declarations: [
    TokenShopComponent,
    RejectTokenComponent,
    BuyTokenComponent
  ],
  imports: [
    CommonModule
  ]
})
export class TokenShopModule { }
