import { Component, Input, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { AppService } from 'src/app/shared/services/app.service';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { Cpu } from '../../shared/models/cpu.model';

@Component({
  selector: 'app-info-cpu',
  templateUrl: './info-cpu.component.html',
  styleUrls: ['./info-cpu.component.scss']
})
export class InfoCpuComponent extends OnDestroyMixin implements OnInit {

  @Input()
  cpu: Cpu = new Cpu();
  @Input()
  cpuId: number;
  showBonus: boolean[] = [true, true, true, true, true, false]

  constructor(private appService: AppService) {
  super();
  }

  ngOnInit(): void {
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.cpu = board_state.CPUS[this.cpuId];
    });
  }

}
