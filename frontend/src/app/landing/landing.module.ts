import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule} from '@angular/router';
import {LandingRoutes} from './landing.routing';
import {LandingComponent} from './components/landing/landing.component';

@NgModule({
    imports: [
        CommonModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        RouterModule.forChild(LandingRoutes),
    ],
    declarations: [
        LandingComponent,
    ],
    exports: [
    ],
    providers: []
})
export class LandingModule { }
