import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';
import {RegistrationLayoutComponent} from './components/registration-layout/registration-layout.component';
import { LandingLayoutComponent } from './components/landing-layout/landing-layout.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
  ],
  declarations: [
    RegistrationLayoutComponent,
    MainLayoutComponent,
    LandingLayoutComponent
  ],
  providers: []
})
export class LayoutModule { }
