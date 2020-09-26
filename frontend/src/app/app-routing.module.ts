import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {RegistrationLayoutComponent} from './layout/components/registration-layout/registration-layout.component';
import {LandingLayoutComponent} from './layout/components/landing-layout/landing-layout.component';
import {MainLayoutComponent} from './layout/components/main-layout/main-layout.component';
import {AuthGuardService} from "./registration/auth.guard";
import {NotFoundComponent} from "./shared/components/not-found/not-found.component";


const routes: Routes = [
  {
    path: '',
    component: LandingLayoutComponent,
    children: [
      {
        path: '',
        loadChildren: () => import('./landing/landing.module').then(m => m.LandingModule)
      }
    ]
  },
  {
    path: '',
    canActivate: [AuthGuardService],
    canActivateChild: [AuthGuardService],
    component: RegistrationLayoutComponent,
    children: [
      {
        path: '',
        loadChildren: () => import('./registration/registration.module').then(m => m.RegistrationModule)
      }
    ]
  },
  {
    path: '',
    canActivate: [AuthGuardService],
    canActivateChild: [AuthGuardService],
    component: MainLayoutComponent,
    children: [
      {
        path: '',
        loadChildren: () => import('./main/main.module').then(m => m.MainModule)
      }
    ]
  },
  {
    path: '**',
    component: NotFoundComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
