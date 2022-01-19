import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RandomTasksComponent } from './random-tasks.component';

describe('RandomTasksComponent', () => {
  let component: RandomTasksComponent;
  let fixture: ComponentFixture<RandomTasksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RandomTasksComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RandomTasksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
