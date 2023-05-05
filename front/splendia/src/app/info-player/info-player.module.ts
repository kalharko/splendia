import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservedCardsComponent } from './reserved-cards/reserved-cards.component';
import { InfoPlayerComponent } from './info-player/info-player.component';
import { InfoPlayersComponent } from './info-players/info-players.component';
import { SharedModule } from '../shared/shared.module';



@NgModule({
  declarations: [
    ReservedCardsComponent,
    InfoPlayerComponent,
    InfoPlayersComponent
  ],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports:[
    InfoPlayerComponent
  ]
})
export class InfoPlayerModule { }
