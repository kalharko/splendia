import { Component, Input, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { Patron } from 'src/app/shared/models/patron.model';
import { AppService } from 'src/app/shared/services/app.service';

@Component({
  selector: 'app-patron-shop',
  templateUrl: './patron-shop.component.html',
  styleUrls: ['./patron-shop.component.scss']
})
export class PatronShopComponent extends OnDestroyMixin implements OnInit {

  // Patrons to display
  patrons: Patron[];

  constructor(private appService: AppService) { 
    super();
  }

  ngOnInit(): void {
    // Subscribe to board_state.patrons
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.patrons = board_state.patrons;
    });
  }
}
