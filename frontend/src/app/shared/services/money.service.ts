import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {RequestsService} from './requests.service';
import {DateTimeService} from "./date-time.service";

@Injectable({
  providedIn: 'root',
})
export class MoneyService {
  constructor(
    private requestsService: RequestsService,
    private dateTimeService: DateTimeService
  ) {}

  public static formatMoney(money, currency) {
    const formatOptions = { style: 'currency', currency, minimumFractionDigits: 2 };
    const userLanguage = (navigator.languages && navigator.languages.length) ? navigator.languages[0] :
      navigator.language || 'en';

    return new Intl.NumberFormat(userLanguage, formatOptions).format(money);
  }

  private adjustDate(date: Date, currency) {
    switch (currency) {
      case 'PLN':
        const days = date.getDay() === 1 ? -3 : -1;
        return this.dateTimeService.addDaysToDate(date, days);
        break;
    }
    return date;
  }

  public getExchangedValue(val: number, date: Date, currencyFrom: string, currencyTo: string) {
    if (currencyFrom !== currencyTo) {
      const adjustedDate = this.adjustDate(date, currencyTo);
      return this.getExchangeRate(adjustedDate, currencyFrom, currencyTo).pipe(
      map((response) => {
        return response * val;
      })
    );
    }
  }

  public getExchangeRate(date: Date, currencyFrom: string, currencyTo: string) {
    const dateStr = date.toISOString().split('T')[0];
    return this.requestsService.getRequest(
      `exchange/?date=${dateStr}&from=${currencyFrom}&to=${currencyTo}`).pipe(
      map((response) => {
        return Number(response);
      })
    );
  }
}
