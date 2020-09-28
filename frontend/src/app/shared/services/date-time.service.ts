import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class DateTimeService {
  constructor() {}

  public sortByDateDesc(a, b) {
    if (a.date > b.date) { return -1; }
    if (a.date < b.date) { return 1; }
  }
}
