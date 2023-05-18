import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservedCardsComponent } from './reserved-cards/reserved-cards.component';
import { ReservedCardComponent } from './reserved-card/reserved-card.component';
import { InfoPlayerComponent } from './info-player/info-player.component';
import { InfoCpuComponent } from './info-cpu/info-cpu.component';
import { SharedModule } from '../shared/shared.module';



@NgModule({
  declarations: [
    ReservedCardComponent,
    ReservedCardsComponent,
    InfoPlayerComponent,
    InfoCpuComponent
  ],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports:[
    InfoPlayerComponent,
    InfoCpuComponent,
    ReservedCardComponent,
    ReservedCardsComponent
  ]
})
export class InfoPlayerModule { }
