import { Component, Input, OnInit } from '@angular/core';
import { ColorsEnum } from '../../enums/colors.enum';

@Component({
  selector: 'app-token',
  templateUrl: './token.component.html',
  styleUrls: ['./token.component.scss']
})

export class TokenComponent implements OnInit {

  @Input() color!:ColorsEnum ;
  @Input() quantity!: string ;

  colorsEnum = ColorsEnum;

  constructor() { 
    console.log(this.color);
  }

  ngOnInit(): void {
  }

}
