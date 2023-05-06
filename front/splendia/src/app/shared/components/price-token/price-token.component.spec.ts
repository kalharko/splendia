import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PriceTokenComponent } from './price-token.component';

describe('PriceTokenComponent', () => {
  let component: PriceTokenComponent;
  let fixture: ComponentFixture<PriceTokenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PriceTokenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PriceTokenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
