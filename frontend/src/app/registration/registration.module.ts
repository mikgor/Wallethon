import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule} from '@angular/router';
import {RegistrationRoutes} from './registration.routing';
import {RegistrationComponent} from './components/registration/registration/registration.component';

@NgModule({
    imports: [
        CommonModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        RouterModule.forChild(RegistrationRoutes),
    ],
    declarations: [
        RegistrationComponent,
    ],
    exports: [
    ],
    providers: []
})
export class RegistrationModule { }
