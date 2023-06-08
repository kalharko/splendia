import { Component, Input, OnInit } from '@angular/core';
import { Card } from 'src/app/shared/models/card.model';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { AppService } from 'src/app/shared/services/app.service';
import { BoardState } from 'src/app/shared/models/board_state.model';

@Component({
  selector: 'app-reserved-card',
  templateUrl: './reserved-card.component.html',
  styleUrls: ['./reserved-card.component.scss']
})
export class ReservedCardComponent extends OnDestroyMixin implements OnInit {

  @Input() position: number;
  card: Card = new Card();
  constructor(private appService: AppService) {
    super();
  }

  ngOnInit(): void {
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.card = board_state.humanPlayer.reservedCards[this.position];
    });
  }

  buyCard(){
    console.log("buy")
    this.appService.buyCard(this.card.cardId);
  }

  getImagePath(): string {
    if(this.card)
      return "url(../../../assets/images/cards/" + this.card.cardId + ".png)"
    return "";
  }

}
