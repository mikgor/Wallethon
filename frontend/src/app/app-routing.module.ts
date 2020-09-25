import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {RegistrationLayoutComponent} from './layout/components/registration-layout/registration-layout.component';
import {LandingLayoutComponent} from './layout/components/landing-layout/landing-layout.component';
import {MainLayoutComponent} from "./layout/components/main-layout/main-layout.component";


const routes: Routes = [
  {
    path: '',
    component: LandingLayoutComponent,
    pathMatch: 'full',
    children: [
      {
        path: '',
        loadChildren: () => import('./landing/landing.module').then(m => m.LandingModule)
      }
    ]
  },
  {
    path: '',
    component: RegistrationLayoutComponent,
    pathMatch: 'full',
    children: [
      {
        path: '',
        loadChildren: () => import('./registration/registration.module').then(m => m.RegistrationModule)
      }
    ]
  },
  {
    path: '',
    component: MainLayoutComponent,
    pathMatch: 'full',
    children: [
      {
        path: '',
        loadChildren: () => import('./main/main.module').then(m => m.MainModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
