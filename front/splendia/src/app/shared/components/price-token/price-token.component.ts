import { Component, OnInit } from '@angular/core';
import { ColorsEnum } from '../../enums/colors.enum';

@Component({
  selector: 'app-price-token',
  templateUrl: './price-token.component.html',
  styleUrls: ['./price-token.component.scss']
})
export class PriceTokenComponent implements OnInit {

  tokenQuantities = [0,0,0,0,0];
  colorsEnum = ColorsEnum;
  constructor() { 
    
  }

  ngOnInit(): void {
  }


}
