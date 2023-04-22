import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PatronShopComponent } from './patron-shop.component';

describe('PatronShopComponent', () => {
  let component: PatronShopComponent;
  let fixture: ComponentFixture<PatronShopComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PatronShopComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PatronShopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
