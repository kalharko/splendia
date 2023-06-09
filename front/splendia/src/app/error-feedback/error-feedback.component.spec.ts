import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ErrorFeedbackComponent } from './error-feedback.component';

describe('ErrorFeedbackComponent', () => {
  let component: ErrorFeedbackComponent;
  let fixture: ComponentFixture<ErrorFeedbackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ErrorFeedbackComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ErrorFeedbackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
