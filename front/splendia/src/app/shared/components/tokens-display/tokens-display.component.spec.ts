import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TokensDisplayComponent } from './tokens-display.component';

describe('TokensDisplayComponent', () => {
  let component: TokensDisplayComponent;
  let fixture: ComponentFixture<TokensDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TokensDisplayComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TokensDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
