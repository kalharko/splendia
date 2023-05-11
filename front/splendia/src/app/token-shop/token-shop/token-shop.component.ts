import { ApplicationInitStatus, Component, OnInit } from '@angular/core';
import { OnDestroyMixin, untilComponentDestroyed } from '@w11k/ngx-componentdestroyed';
import { ColorsEnum } from 'src/app/shared/enums/colors.enum';
import { BoardState } from 'src/app/shared/models/board_state.model';
import { AppService } from 'src/app/shared/services/app.service';
import { ColorsEnumUtil } from 'src/app/shared/utils/colors-enum-util';

@Component({
  selector: 'app-token-shop',
  templateUrl: './token-shop.component.html',
  styleUrls: ['./token-shop.component.scss']
})
export class TokenShopComponent extends OnDestroyMixin implements OnInit {

  // token quantities to display
  tokenQuantities: number[];

  constructor(private appService: AppService) { 
    super();
  }

  ngOnInit(): void {
    // Subscribe to board_state.bank
    this.appService.board_state.pipe(untilComponentDestroyed(this)).subscribe((board_state:BoardState) => {
      this.tokenQuantities = board_state.bank;
    });
  }

  getCssTokenClassOfColor(tokenColor: ColorsEnum): string {
    return ColorsEnumUtil.getCssTokenClassOfColor(tokenColor);
  }
}
