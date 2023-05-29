import { Component, OnInit } from '@angular/core';
import { AppService } from 'src/app/shared/services/app.service';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { BoardState } from 'src/app/shared/models/board_state.model';

@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.scss']
})
export class LogsComponent extends OnDestroyMixin implements OnInit {

    logs: string[];

    constructor(private appService: AppService) {
      super()
  }

  ngOnInit(): void {
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.logs = board_state.logs;
    });

  }

}
