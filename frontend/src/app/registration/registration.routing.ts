import {Routes} from '@angular/router';
import {APP_ROUTES} from '../routes-config';
import {RegistrationComponent} from './components/registration/registration/registration.component';


export const RegistrationRoutes: Routes = [
    { path: `${APP_ROUTES.registration}`, component: RegistrationComponent },
  ];
