import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservedCardsComponent } from './reserved-cards/reserved-cards.component';
import { InfoPlayerComponent } from './info-player/info-player.component';
import { InfoCpuComponent } from './info-cpu/info-cpu.component';
import { SharedModule } from '../shared/shared.module';



@NgModule({
  declarations: [
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
    InfoCpuComponent
  ]
})
export class InfoPlayerModule { }
