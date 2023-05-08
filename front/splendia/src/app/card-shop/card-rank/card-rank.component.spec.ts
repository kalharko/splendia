import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardRankComponent } from './card-row.component';

describe('CardRowComponent', () => {
  let component: CardRankComponent;
  let fixture: ComponentFixture<CardRankComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CardRankComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CardRankComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
