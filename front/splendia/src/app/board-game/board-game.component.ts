import { Component, OnInit } from '@angular/core';
import { AppService } from 'src/app/shared/services/app.service';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { BoardState } from 'src/app/shared/models/board_state.model';

@Component({
  selector: 'app-board-game',
  templateUrl: './board-game.component.html',
  styleUrls: ['./board-game.component.scss']
})
export class BoardGameComponent extends OnDestroyMixin implements OnInit {

    board_state: BoardState= new BoardState();

    constructor(private appService: AppService) {
      super();
  }

  ngOnInit(): void {
    this.appService.launchGame();
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.board_state = board_state;
    });

  }

}
