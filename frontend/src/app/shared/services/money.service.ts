import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class MoneyService {
  constructor() {}

  public formatMoney(money, currency) {
    const formatOptions = { style: 'currency', currency, minimumFractionDigits: 4 };
    const userLanguage = (navigator.languages && navigator.languages.length) ? navigator.languages[0] :
      navigator.language || 'en';

    return new Intl.NumberFormat(userLanguage, formatOptions).format(money);
  }
}
