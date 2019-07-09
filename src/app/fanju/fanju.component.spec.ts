import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FanjuComponent } from './fanju.component';

describe('FanjuComponent', () => {
  let component: FanjuComponent;
  let fixture: ComponentFixture<FanjuComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FanjuComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FanjuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
