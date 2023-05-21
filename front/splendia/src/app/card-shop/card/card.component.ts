import { Component, Input, OnInit } from '@angular/core';
import { Card } from 'src/app/shared/models/card.model';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { AppService } from 'src/app/shared/services/app.service';
import { BoardState } from 'src/app/shared/models/board_state.model';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss']
})
export class CardComponent extends OnDestroyMixin implements OnInit {

  @Input() rankNumber: number;
  @Input() cardNumber: number;
  card: Card = new Card();
  constructor(private appService: AppService) {
    super();
  }

  ngOnInit(): void {
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.card = board_state.shop[this.rankNumber].visibleCards[this.cardNumber];
    });
  }

  buyCard(){
    this.appService.buyCard(this.card.cardId);
  }

  reserveCard(){
    this.appService.reserveCard(this.card.cardId);
  }

  getImagePath(): string {
    return "url(../../../assets/images/cards/" + this.card.cardId + ".png)"
  }

}
