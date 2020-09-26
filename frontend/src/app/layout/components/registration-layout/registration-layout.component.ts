import { Component, OnInit } from '@angular/core';
import {APP_ROUTES} from '../../../routes-config';

@Component({
  selector: 'app-registration-layout',
  templateUrl: './registration-layout.component.html',
  styleUrls: ['./registration-layout.component.scss']
})
export class RegistrationLayoutComponent implements OnInit {
  APP_ROUTES = APP_ROUTES;

  constructor() { }

  ngOnInit(): void {
  }

}
