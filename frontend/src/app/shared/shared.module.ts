import {NgModule} from '@angular/core';
import {MaterialModule} from '../material.module';
import { NotFoundComponent } from './components/not-found/not-found.component';

@NgModule({
  imports: [
    MaterialModule
  ],
  exports: [
    MaterialModule
  ],
  declarations: [NotFoundComponent]
})
export class SharedModule {}
