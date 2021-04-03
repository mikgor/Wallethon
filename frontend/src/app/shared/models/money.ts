import {MONEY_FRACTION_DIGITS} from '../../config';

export class Money {
  amount: number;
  currency: string;

  public constructor(amount: number, currency: string = '') {
    this.amount = Number(amount);
    this.currency = currency;
  }

  public sum(money: Money) {
    this.currency = this.currencyEquals('') ? money.currency : this.currency;
    money.currency = money.currencyEquals('') ? this.currency : money.currency;
    const amount = this.amount + money.amount;
    return new Money(amount, this.currency);
  }

  public subtract(money: Money) {
    const moneyCopy = new Money(money.amount, money.currency);
    moneyCopy.amount *= -1;
    return this.sum(moneyCopy);
  }

  public multiply(factor: number) {
    const amount = this.amount * factor;
    return new Money(amount, this.currency);
  }

  public currencyEquals(currency: string) {
    return currency === this.currency;
  }

  public toRepresentation() {
    const currency = this.currency;
    const formatOptions = { style: 'currency', currency, minimumFractionDigits: MONEY_FRACTION_DIGITS };
    const userLanguage = (navigator.languages && navigator.languages.length) ? navigator.languages[0] :
      navigator.language || 'en';

    return currency === '' ? this.amount : new Intl.NumberFormat(userLanguage, formatOptions).format(this.amount);
  }
}
