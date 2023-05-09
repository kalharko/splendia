import { Component, Input, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { Patron } from 'src/app/shared/models/patron.model';
import { AppService } from 'src/app/shared/services/app.service';

@Component({
  selector: 'app-patron-card',
  templateUrl: './patron-card.component.html',
  styleUrls: ['./patron-card.component.scss']
})
export class PatronCardComponent extends OnDestroyMixin implements OnInit {
url(arg0: string): any {
throw new Error('Method not implemented.');
}
  // Corresponds to the position of the patron card in board_state.patrons
  @Input() patronNumberList:number;
  // Patron to display
  patron: Patron;

  constructor(private appService: AppService) { 
    super();
  }

  ngOnInit(): void {
    // Subscribe to board_state.patrons[this.patronNumberList]
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.patron = board_state.patrons[this.patronNumberList];
      console.log(this.patron.patronId);
    });
  }

}
