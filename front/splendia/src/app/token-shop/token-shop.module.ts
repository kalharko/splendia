import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TokenShopComponent } from './token-shop/token-shop.component';
import { RejectTokenComponent } from './reject-token/reject-token.component';
import { BuyTokenComponent } from './buy-token/buy-token.component';
import { SharedModule } from '../shared/shared.module';
import { MatDialogModule } from '@angular/material/dialog';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";



@NgModule({
  declarations: [
    TokenShopComponent,
    RejectTokenComponent,
    BuyTokenComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    MatDialogModule,
    BrowserAnimationsModule
  ],
  exports:[
    TokenShopComponent
  ]
})
export class TokenShopModule { }
