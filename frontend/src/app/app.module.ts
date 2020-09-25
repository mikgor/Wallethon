import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule} from '@angular/router';
import {LayoutModule} from './layout/layout.module';
import {RegistrationModule} from './registration/registration.module';
import {LandingModule} from './landing/landing.module';
import {MainModule} from './main/main.module';


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    RouterModule,
    AppRoutingModule,
    LayoutModule,
    MainModule,
    RegistrationModule,
    LandingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
