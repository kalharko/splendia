import { Component, Input, OnInit } from '@angular/core';
import { ColorsEnum } from '../../enums/colors.enum';
import { colorsEnumToString } from '../../utils/colors-enum-utils';

@Component({
  selector: 'app-token',
  templateUrl: './token.component.html',
  styleUrls: ['./token.component.scss']
})

export class TokenComponent implements OnInit {
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
