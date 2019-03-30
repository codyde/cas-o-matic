import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RemoveorgComponent } from './removeorg.component';

describe('RemoveorgComponent', () => {
  let component: RemoveorgComponent;
  let fixture: ComponentFixture<RemoveorgComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RemoveorgComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RemoveorgComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
