import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TokenComponent } from './components/token/token.component';
import { TokensDisplayComponent } from './components/tokens-display/tokens-display.component';
import { PriceTokenComponent } from './components/price-token/price-token.component';
import {HttpClientModule} from '@angular/common/http';


@NgModule({
  imports:[CommonModule,
    HttpClientModule],
  declarations: [
    TokenComponent,
    TokensDisplayComponent,
    PriceTokenComponent],
  exports:[
    TokenComponent,
    TokensDisplayComponent,
    PriceTokenComponent,
  ]
})
export class SharedModule { }
