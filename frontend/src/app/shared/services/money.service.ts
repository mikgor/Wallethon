import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {RequestsService} from './requests.service';
import {DateTimeService} from './date-time.service';
import {MONEY_FRACTION_DIGITS, STOCK_FRACTION_DIGITS} from '../../config';
import {Currency} from '../models/currency';
import {Money} from '../models/money';

@Injectable({
  providedIn: 'root',
})
export class MoneyService {
  constructor(
    private requestsService: RequestsService,
    private dateTimeService: DateTimeService
  ) {}

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

  public getExchangedValue(val: Money, date: Date, currencyTo: string) {
    if (val.currency !== currencyTo) {
      const adjustedDate = this.adjustDate(date, currencyTo);
      return this.getExchangeRate(adjustedDate, val.currency, currencyTo).pipe(
        map((response) => {
          let exchangedValue = response * val.amount;
          let multiplier = 1;
          if (exchangedValue < 0) {
            multiplier = -1;
            exchangedValue *=  -1;
          }
          return new Money(Number(exchangedValue.toFixed(MONEY_FRACTION_DIGITS)) * multiplier, currencyTo);
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

  public getExchangeCurrencies() {
    return this.requestsService.getRequest(`currencies/`).pipe(
      map((response) => {
        return [new Currency('USD', 'USD'), new Currency('PLN', 'PLN')];
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
