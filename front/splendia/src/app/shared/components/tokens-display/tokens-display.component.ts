import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-tokens-display',
  templateUrl: './tokens-display.component.html',
  styleUrls: ['./tokens-display.component.scss']
})
export class TokensDisplayComponent implements OnInit {
  // token quantities to display
  @Input() tokenQuantities: number[];

   /**
    * boolean array that dictates if a token should be displayed or not.
    * example: [true, false, true, false, true, true}] will display all tokens except the blue and red ones
    */
  @Input() showTokens: boolean[];


  constructor() { }

  ngOnInit(): void {
  }

}
