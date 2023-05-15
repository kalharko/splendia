import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardShopComponent } from './card-shop/card-shop.component';
import { DeckComponent } from './deck/deck.component';
import { CardComponent } from './card/card.component';
import { SharedModule } from '../shared/shared.module';
import { CardRankComponent } from './card-rank/card-rank.component';



@NgModule({
  declarations: [
    CardShopComponent,
    CardRankComponent,
    DeckComponent,
    CardComponent
  ],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports: [
    CardShopComponent
  ]
})
export class CardShopModule { }
