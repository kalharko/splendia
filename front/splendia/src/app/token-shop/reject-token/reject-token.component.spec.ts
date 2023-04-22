import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RejectTokenComponent } from './reject-token.component';

describe('RejectTokenComponent', () => {
  let component: RejectTokenComponent;
  let fixture: ComponentFixture<RejectTokenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RejectTokenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RejectTokenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
