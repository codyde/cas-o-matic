import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgdataComponent } from './orgdata.component';

describe('OrgdataComponent', () => {
  let component: OrgdataComponent;
  let fixture: ComponentFixture<OrgdataComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrgdataComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrgdataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
