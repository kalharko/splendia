import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardShopComponent } from './card-shop/card-shop.component';
import { CardRowComponent } from './card-row/card-row.component';
import { DeckComponent } from './deck/deck.component';
import { CardComponent } from './card/card.component';



@NgModule({
  declarations: [
    CardShopComponent,
    CardRowComponent,
    DeckComponent,
    CardComponent
  ],
  imports: [
    CommonModule
  ]
})
export class CardShopModule { }
