import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReservedCardComponent } from './reserved-card.component';

describe('CardComponent', () => {
  let component: ReservedCardComponent;
  let fixture: ComponentFixture<ReservedCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReservedCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReservedCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
