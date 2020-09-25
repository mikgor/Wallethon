import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule} from '@angular/router';
import {MainRoutes} from './main.routing';
import {DashboardComponent} from './components/dashboard/dashboard.component';

@NgModule({
    imports: [
        CommonModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        RouterModule.forChild(MainRoutes),
    ],
    declarations: [
        DashboardComponent,
    ],
    exports: [
    ],
    providers: []
})
export class MainModule { }
