import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservedCardsComponent } from './reserved-cards/reserved-cards.component';
import { InfoPlayerComponent } from './info-player/info-player.component';
import { InfoPlayersComponent } from './info-players/info-players.component';



@NgModule({
  declarations: [
    ReservedCardsComponent,
    InfoPlayerComponent,
    InfoPlayersComponent
  ],
  imports: [
    CommonModule
  ]
})
export class InfoPlayerModule { }
