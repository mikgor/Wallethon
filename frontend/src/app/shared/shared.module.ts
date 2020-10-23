import {NgModule} from '@angular/core';
import {MaterialModule} from '../material.module';
import { NotFoundComponent } from './components/not-found/not-found.component';
import { BaseAddEditPageComponent } from './components/base-add-edit-page/base-add-edit-page.component';

@NgModule({
  imports: [
    MaterialModule
  ],
  exports: [
    MaterialModule
  ],
  declarations: [NotFoundComponent, BaseAddEditPageComponent]
})
export class SharedModule {}
