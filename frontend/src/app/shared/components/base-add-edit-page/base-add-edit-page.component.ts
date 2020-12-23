import { Component } from '@angular/core';
import {FormGroup} from '@angular/forms';
import {ApiResponseHandlingService} from '../../services/api-response-handling.service';
import {HttpErrorResponse} from '@angular/common/http';

@Component({
  selector: 'app-base-add-edit-page',
  templateUrl: './base-add-edit-page.component.html',
  styleUrls: ['./base-add-edit-page.component.scss']
})
export class BaseAddEditPageComponent{
  public form: FormGroup;
  public submit = false;
  public errorMessage = '';

  constructor(public apiResponseHandlingService: ApiResponseHandlingService) { }

  public isFormValid() {
    this.submit = true;
    this.form.markAllAsTouched();

    return !this.form.invalid;
  }

  public get controls() {
    return this.form.controls;
  }

  public getErrorMessage(error: HttpErrorResponse) {
    this.errorMessage = this.apiResponseHandlingService.getErrorMessage(error.error);
  }
}
