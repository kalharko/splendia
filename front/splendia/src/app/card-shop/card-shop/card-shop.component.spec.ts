import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardShopComponent } from './card-shop.component';

describe('CardShopComponent', () => {
  let component: CardShopComponent;
  let fixture: ComponentFixture<CardShopComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CardShopComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CardShopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
