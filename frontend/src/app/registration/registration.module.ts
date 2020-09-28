import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule} from '@angular/router';
import {RegistrationRoutes} from './registration.routing';
import {RegistrationComponent} from './components/registration/registration/registration.component';
import { LoginComponent } from './components/login/login.component';
import {SharedModule} from '../shared/shared.module';

@NgModule({
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forChild(RegistrationRoutes),
    SharedModule,
  ],
  declarations: [
    RegistrationComponent,
    LoginComponent,
  ],
  exports: [
  ],
  providers: []
})
export class RegistrationModule { }
