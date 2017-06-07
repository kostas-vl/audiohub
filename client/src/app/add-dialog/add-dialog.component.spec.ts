import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddFolderDialogComponent } from './add-dialog.component';

describe('AddFolderDialogComponent', () => {
    let component: AddFolderDialogComponent;
    let fixture: ComponentFixture<AddFolderDialogComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [AddFolderDialogComponent]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(AddFolderDialogComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
