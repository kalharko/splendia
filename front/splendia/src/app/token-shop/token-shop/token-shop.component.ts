import { ApplicationInitStatus, Component, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { ColorsEnum } from 'src/app/shared/enums/colors.enum';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { AppService } from 'src/app/shared/services/app.service';

@Component({
  selector: 'app-token-shop',
  templateUrl: './token-shop.component.html',
  styleUrls: ['./token-shop.component.scss']
})
export class TokenShopComponent extends OnDestroyMixin implements OnInit  {

  tokenQuantities : number[];

  colorEnum:ColorsEnum;

  constructor(private appService: AppService) { 
    super();
  
  }

  ngOnInit(): void {
    this.appService.takeToken().pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.tokenQuantities = board_state.shop.tokens._tokens;
    });
  }
}
