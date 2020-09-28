import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {API_URL} from '../../config';
import {catchError} from 'rxjs/operators';
import {AuthService} from '../../registration/services/auth.service';
import {Router} from '@angular/router';
import {APP_ROUTES} from 'src/app/routes-config';

@Injectable({
  providedIn: 'root',
})
export class RequestsService {
  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private router: Router,
  ) {}

  public getRequest(endpoint: string) {
    return this.http.get(`${API_URL}/${endpoint}`).pipe(
      catchError(error => {
        this.onRequestError(error);
        return error;
      })
    );
  }

  public onRequestError(error) {
    if (error.error.detail === 'Invalid token.') {
      this.authService.logoutUser();
      this.router.navigate([APP_ROUTES.login]);
    }
  }
}
