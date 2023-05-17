import { Component, Input, OnInit } from '@angular/core';
import { AppService } from 'src/app/shared/services/app.service';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { Player } from 'src/app/shared/models/player.model';

@Component({
  selector: 'app-info-player',
  templateUrl: './info-player.component.html',
  styleUrls: ['./info-player.component.scss']
})
export class InfoPlayerComponent extends OnDestroyMixin implements OnInit {

  @Input()
  player: Player = new Player();
  constructor(private appService: AppService) {
  super();
  }

  ngOnInit(): void {
      this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.player = board_state.humanPlayer;
    });
  }

}
