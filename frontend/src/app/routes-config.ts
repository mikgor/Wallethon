export enum APP_ROUTES {
  // Registration
  registration = 'app/registration',
  login = 'app/login',

  // Main
  dashboard = 'app/dashboard',

  // Landing
  landing = 'home',
}

export enum PermissionRule {
  Any,
  None,
  Anonymous,
  Authenticated
}

export const PERMISSIONS_RULE_REDIRECTS = [
  {rule: PermissionRule.Authenticated, redirect: APP_ROUTES.login},
  {rule: PermissionRule.Anonymous, redirect: APP_ROUTES.dashboard},
];

export class RouteConfig {
  name: string;
  route: string;
  rule: PermissionRule;
}

export const ROUTES_PERMISSIONS: RouteConfig[] = [
  {name: 'Registration', route: APP_ROUTES.registration, rule: PermissionRule.Anonymous},
  {name: 'Login', route: APP_ROUTES.login, rule: PermissionRule.Anonymous},
];

export const DEFAULT_ROUTE_PERMISSION = PermissionRule.Authenticated;
export const DEFAULT_ROUTE_REDIRECT = APP_ROUTES.login;
