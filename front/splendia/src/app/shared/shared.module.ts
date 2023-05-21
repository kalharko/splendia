import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TokenComponent } from './components/token/token.component';
import { BonusComponent } from './components/bonus/bonus.component';
import { TokensDisplayComponent } from './components/tokens-display/tokens-display.component';
import { PriceTokenComponent } from './components/price-token/price-token.component';
import {HttpClientModule} from '@angular/common/http';


@NgModule({
  imports:[CommonModule,
    HttpClientModule],
  declarations: [
    TokenComponent,
    BonusComponent,
    TokensDisplayComponent,
    PriceTokenComponent],
  exports:[
    TokenComponent,
    BonusComponent,
    TokensDisplayComponent,
    PriceTokenComponent,
  ]
})
export class SharedModule { }
