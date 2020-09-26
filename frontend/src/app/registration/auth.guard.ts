import { Injectable } from '@angular/core';
import {Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, CanActivateChild} from '@angular/router';
import {AuthService} from './services/auth.service';
import {
  DEFAULT_ROUTE_PERMISSION,
  DEFAULT_ROUTE_REDIRECT,
  PermissionRuleRedirect,
  ROUTES_PERMISSIONS
} from '../routes-config';


@Injectable({ providedIn: 'root' })
export class AuthGuardService implements CanActivate, CanActivateChild {

  constructor(private router: Router,
              private authService: AuthService) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    const url = state.url.substring(1).replace('?', '');
    const routeAccessConfig = ROUTES_PERMISSIONS.find(x => x.route === url);
    const rule = routeAccessConfig ? routeAccessConfig.rule : DEFAULT_ROUTE_PERMISSION;
    if (!this.authService.userHasAccess(rule)) {
      const redirect = PermissionRuleRedirect.find(x => x.rule === rule);
      const redirectRoute = redirect ? redirect.redirect : DEFAULT_ROUTE_REDIRECT;
      this.router.navigate([`/${redirectRoute}`], { queryParams: { retUrl: route.url} });
      return false;
    }

    return true;
  }

  canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    return this.canActivate(route, state);
  }
}
