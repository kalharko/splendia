import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BoardGameComponent } from './board-game/board-game.component';
import { PatronShopModule } from './patron-shop/patron-shop.module';
import { SharedModule } from './shared/shared.module';
import { InfoPlayerComponent } from './info-player/info-player/info-player.component';
import { InfoPlayerModule } from './info-player/info-player.module';
import { CardShopModule } from './card-shop/card-shop.module';
import { TokenShopComponent } from './token-shop/token-shop/token-shop.component';
import { TokenShopModule } from './token-shop/token-shop.module';
import { CommonModule } from '@angular/common';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";


@NgModule({
  declarations: [
    AppComponent,
    BoardGameComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    AppRoutingModule,

    PatronShopModule,
    InfoPlayerModule,
    CardShopModule,
    TokenShopModule,

    SharedModule
  ],
  exports: [
    SharedModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
