import {Routes} from '@angular/router';
import {APP_ROUTES} from '../routes-config';
import {LandingComponent} from './components/landing/landing.component';


export const LandingRoutes: Routes = [
    { path: `${APP_ROUTES.landing}`, component: LandingComponent },
  ];
