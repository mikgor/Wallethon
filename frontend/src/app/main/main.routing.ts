import {Routes} from '@angular/router';
import {APP_ROUTES} from '../routes-config';
import {DashboardComponent} from './components/dashboard/dashboard.component';


export const MainRoutes: Routes = [
    { path: `${APP_ROUTES.dashboard}`, component: DashboardComponent },
  ];
