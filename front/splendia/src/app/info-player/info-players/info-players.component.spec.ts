import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoPlayersComponent } from './info-players.component';

describe('InfoPlayersComponent', () => {
  let component: InfoPlayersComponent;
  let fixture: ComponentFixture<InfoPlayersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InfoPlayersComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InfoPlayersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
