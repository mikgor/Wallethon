import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';
import {RegistrationLayoutComponent} from './components/registration-layout/registration-layout.component';
import {FormsModule} from '@angular/forms';
import {MainModule} from '../main/main.module';
import {LandingLayoutComponent} from './components/landing-layout/landing-layout.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MainModule,
  ],
  declarations: [
    RegistrationLayoutComponent,
    LandingLayoutComponent,
    MainLayoutComponent
  ],
  exports: [RegistrationLayoutComponent],
  providers: []
})
export class LayoutModule { }
