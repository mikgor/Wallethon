import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule} from '@angular/router';
import {MainRoutes} from './main.routing';
import {DashboardComponent} from './components/dashboard/dashboard.component';
import {SharedModule} from '../shared/shared.module';

@NgModule({
    imports: [
        CommonModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        RouterModule.forChild(MainRoutes),
        SharedModule,
    ],
    declarations: [
        DashboardComponent,
    ],
    exports: [
    ],
    providers: []
})
export class MainModule { }
