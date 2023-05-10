import { Component, Input, OnInit } from '@angular/core';
import { Patron } from 'src/app/shared/models/patron.model';


@Component({
  selector: 'app-patron-card',
  templateUrl: './patron-card.component.html',
  styleUrls: ['./patron-card.component.scss']
})
export class PatronCardComponent implements OnInit {

  // Patron to display
  @Input() patron: Patron;

  constructor() {}

  ngOnInit(): void {
  }

}
