import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PatronShopComponent } from './patron-shop/patron-shop.component';
import { PatronCardComponent } from './patron-card/patron-card.component';
import { SharedModule } from '../shared/shared.module';
import { BrowserModule } from '@angular/platform-browser';



@NgModule({
  declarations: [
    PatronShopComponent,
    PatronCardComponent
  ],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports: [
    PatronShopComponent
  ]
})
export class PatronShopModule { }
