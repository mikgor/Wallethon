import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {RequestsService} from './requests.service';
import {DateTimeService} from './date-time.service';
import {MONEY_FRACTION_DIGITS, STOCK_FRACTION_DIGITS} from '../../config';
import {Currency} from '../models/currency';

@Injectable({
  providedIn: 'root',
})
export class MoneyService {
  constructor(
    private requestsService: RequestsService,
    private dateTimeService: DateTimeService
  ) {}

  public static formatMoney(money, currency) {
    const formatOptions = { style: 'currency', currency, minimumFractionDigits: MONEY_FRACTION_DIGITS };
    const userLanguage = (navigator.languages && navigator.languages.length) ? navigator.languages[0] :
      navigator.language || 'en';

    return new Intl.NumberFormat(userLanguage, formatOptions).format(money);
  }

  public static formatStock(val: number) {
    return Number(val.toFixed(STOCK_FRACTION_DIGITS));
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
          let exchangedValue = response * val;
          let multiplier = 1;
          if (exchangedValue < 0) {
            multiplier = -1;
            exchangedValue *=  -1;
          }
          return Number(exchangedValue.toFixed(MONEY_FRACTION_DIGITS)) * multiplier;
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

  public getCurrencies() {
    return this.requestsService.getRequest(`currencies/`).pipe(
      map((response) => {
        return this.getCurrenciesFromResponse(response);
      })
    );
  }

  public getCurrenciesFromResponse(response) {
    const currencies: Currency[] = [];
    for (const currency of response) {
      currencies.push(this.getCurrencyFromResponse(currency));
    }
    return currencies;
  }

  public getCurrencyFromResponse(response) {
    return new Currency(
      response.symbol,
      response.name
    );
  }
}
