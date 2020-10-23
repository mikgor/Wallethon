import {AbstractControl} from '@angular/forms';
import {AutoCompleteFilter} from '../models/auto-complete-filter';

export function autoCompleteValidator(autoCompleteFilter: AutoCompleteFilter) {
  return (control: AbstractControl) => {
    return autoCompleteFilter.dataExists(control.value) ? true : null;
  };
}
