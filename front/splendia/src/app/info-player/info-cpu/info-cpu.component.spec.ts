import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoCpuComponent } from './info-cpu.component';

describe('InfoCpuComponent', () => {
  let component: InfoCpuComponent;
  let fixture: ComponentFixture<InfoCpuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InfoCpuComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InfoCpuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
