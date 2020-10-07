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

  public sortByDateAsc(a, b) {
    if (a.date > b.date) { return 1; }
    if (a.date < b.date) { return -1; }
  }

  public addDaysToDate(date: Date, days: number){
    return new Date(date.getTime() + (days * 24 * 60 * 60 * 1000));
  }
}
