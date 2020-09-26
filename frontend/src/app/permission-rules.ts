import {AuthService} from './registration/services/auth.service';
import {Injectable} from '@angular/core';

@Injectable()
export class PermissionRules {
  constructor(private authService: AuthService) {
    this.authService = authService;
  }

  public any() {
    return true;
  }

  public none() {
    return false;
  }

  public anonymous() {
    return this.authService.isUserAnonymous();
  }

  public authenticated() {
    return this.authService.isUserAuthenticated();
  }
}
