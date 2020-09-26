import {Injectable} from '@angular/core';
import {User} from '../models/user';
import {HttpClient, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {PlatformLocation} from '@angular/common';
import {Observable} from 'rxjs';
import {USER_TOKEN_TTL} from '../../config';
import {PermissionRule} from '../../routes-config';


@Injectable()
export class AuthService {
  private readonly backendUrl: string;

  constructor(
    private http: HttpClient,
    private location: PlatformLocation
  ) {
     this.backendUrl = (this.location as any).location.origin;
    }

  public getCurrentUser(): User {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (userData === null) {
      return  null;
    }

    return new User(userData.id, userData.username, userData.token, new Date(userData.tokenExpiration));
  }

  public login(username: string, password: string) {
    this.logoutUser();
    const options = { headers: { 'Content-Type': 'application/json' } };
    const params = { username, password };
    return this.http.post<any>(`${this.backendUrl}/api/v1/login/`, params, options)
      .pipe(
        map((response) => {
          const user = new User(
            response.user,
            username,
            response.token,
            new Date(response.expiry),
          );
          this.saveUser(user);
        })
      );
  }

  public extendUserToken() {
    const updatedExpiration = new Date();
    updatedExpiration.setHours(updatedExpiration.getHours() + USER_TOKEN_TTL);

    const user = this.getCurrentUser();
    user.tokenExpiration = updatedExpiration;
    this.saveUser(user);
  }

  public hasUserTokenExpired() {
    const user = this.getCurrentUser();
    if (user === null) {
      return true;
    }
    return new Date().valueOf() >= user.tokenExpiration.valueOf();
  }

  public saveUser(user: User) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  public logoutUser() {
    localStorage.removeItem('user');
  }

  public isUserAuthenticated() {
    return !this.hasUserTokenExpired();
  }

  public isUserAnonymous() {
    return !this.isUserAuthenticated();
  }

  private userPassesRule(rule: PermissionRule) {
    switch (rule) {
      case PermissionRule.None: {
        return false;
      }
      case PermissionRule.Any: {
        return true;
      }
      case PermissionRule.Authenticated: {
        return this.isUserAuthenticated();
      }
      case PermissionRule.Anonymous: {
        return this.isUserAnonymous();
      }
    }
  }

  public userHasAccess(rule: PermissionRule) {
    return this.userPassesRule(rule);
  }
}

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}


  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser && currentUser.token) {
      this.authService.extendUserToken();
      req = req.clone({
          setHeaders: {
            Authorization: `Token ${currentUser.token}`,
          },
        });
      }

    return next.handle(req);
  }
}
