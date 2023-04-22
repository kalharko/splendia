import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PatronShopComponent } from './patron-shop/patron-shop.component';
import { PatronCardComponent } from './patron-card/patron-card.component';



@NgModule({
  declarations: [
    PatronShopComponent,
    PatronCardComponent
  ],
  imports: [
    CommonModule
  ]
})
export class PatronShopModule { }
