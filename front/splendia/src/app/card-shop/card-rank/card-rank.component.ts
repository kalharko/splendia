import { Component, Input, OnInit } from '@angular/core';
import { Rank } from 'src/app/shared/models/rank.model';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { AppService } from 'src/app/shared/services/app.service';
import { BoardState } from 'src/app/shared/models/board_state.model';

@Component({
  selector: 'app-card-rank',
  templateUrl: './card-rank.component.html',
  styleUrls: ['./card-rank.component.scss']
})
export class CardRankComponent extends OnDestroyMixin implements OnInit {

  @Input() rankNumber:number;
  cardRank: Rank = new Rank();
  constructor(private appService: AppService) { 
    super();
  }

  ngOnInit(): void {
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.cardRank = board_state.shop[this.rankNumber];
    });

  }

}
