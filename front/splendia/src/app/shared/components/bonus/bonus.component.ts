import { Component, Input, OnInit } from '@angular/core';
import { ColorsEnum } from '../../enums/colors.enum';
import { colorsEnumToString } from '../../utils/colors-enum-utils';

@Component({
  selector: 'app-bonus',
  templateUrl: './bonus.component.html',
  styleUrls: ['./bonus.component.scss']
})

export class BonusComponent implements OnInit {
  // Color of the token
  @Input() color: ColorsEnum ;
  // Quantity of the token
  @Input() quantity: number ;
  // Ff true, the token is shown. Otherwise the token is hidden
  @Input() show: boolean ;

  colorsEnum = ColorsEnum;

  constructor() {}

  ngOnInit(): void {
  }

  /**
   * Get the url for the background image of the token
   * @return the background image url
   */
  getBackgroundImageToken(): string {
    return "url(../../../../assets/images/tokens/" + colorsEnumToString(this.color) + ".png)";
  }

  /**
   * Get the text color of the token
   * @return
   */
  getTextColor(): string {
    if(this.color == ColorsEnum.BLACK) {
      return "white";
    }

    return "black";
  }

}
