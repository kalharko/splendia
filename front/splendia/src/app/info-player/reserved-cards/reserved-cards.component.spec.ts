import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReservedCardsComponent } from './reserved-cards.component';

describe('ReservedCardsComponent', () => {
  let component: ReservedCardsComponent;
  let fixture: ComponentFixture<ReservedCardsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReservedCardsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReservedCardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
