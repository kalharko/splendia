import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TokenShopComponent } from './token-shop.component';

describe('TokenShopComponent', () => {
  let component: TokenShopComponent;
  let fixture: ComponentFixture<TokenShopComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TokenShopComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TokenShopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
