import { Component, Input, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { AppService } from 'src/app/shared/services/app.service';

@Component({
  selector: 'app-error-feedback',
  templateUrl: './error-feedback.component.html',
  styleUrls: ['./error-feedback.component.scss']
})
export class ErrorFeedbackComponent extends OnDestroyMixin implements OnInit {

  errorMessage: String;
  constructor(private appService: AppService) {
    super();
  }

  ngOnInit(): void {
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.errorMessage = board_state.gameState.errorMessage;
    });
  }


}

