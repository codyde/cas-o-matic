import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SpcdetailComponent } from './spcdetail.component';

describe('SpcdetailComponent', () => {
  let component: SpcdetailComponent;
  let fixture: ComponentFixture<SpcdetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SpcdetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SpcdetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
