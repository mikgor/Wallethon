import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {AuthService} from '../../services/auth.service';
import {Router} from "@angular/router";
import { APP_ROUTES } from 'src/app/routes-config';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  public loginForm: FormGroup;
  public loading = false;
  public submit = false;
  public invalidCredentials = false;
  public APP_ROUTES = APP_ROUTES;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    ) { }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  onSubmit() {
    this.submit = true;

    this.loginForm.markAllAsTouched();
    if (this.loginForm.invalid) {
      return;
    }
    this.loading = true;
    this.invalidCredentials = false;
    this.authService
      .login(this.loginForm.controls.email.value, this.loginForm.controls.password.value)
      .subscribe(
        () => {
          this.router.navigate([this.APP_ROUTES.dashboard]);
        },
        (error) => {
          this.loading = false;
          this.invalidCredentials = true;
        }
      );
  }
}
