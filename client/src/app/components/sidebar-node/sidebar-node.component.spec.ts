import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarNodeComponent } from './sidebar-node.component';

describe('SidebarNodeComponent', () => {
  let component: SidebarNodeComponent;
  let fixture: ComponentFixture<SidebarNodeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SidebarNodeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidebarNodeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
