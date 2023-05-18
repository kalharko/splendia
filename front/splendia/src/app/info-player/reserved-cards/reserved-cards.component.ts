import { Component, Input, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { AppService } from 'src/app/shared/services/app.service';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { Card } from 'src/app/shared/models/card.model';

@Component({
  selector: 'app-reserved-cards',
  templateUrl: './reserved-cards.component.html',
  styleUrls: ['./reserved-cards.component.scss']
})


export class ReservedCardsComponent extends OnDestroyMixin implements OnInit {

  @Input()
  cards: Card[];

  constructor(private appService: AppService) {
  super();
  }

  ngOnInit(): void {
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.cards = board_state.humanPlayer.reservedCards;
    });
  }

}
