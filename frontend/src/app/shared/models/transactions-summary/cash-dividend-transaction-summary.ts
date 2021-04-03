import {CashDividendTransaction} from '../../../main/components/dashboard/models/CashDividendTransaction';
import {Money} from '../money';

export class CashDividendTransactionSummary {
  cashDividendTransaction: CashDividendTransaction;
  income: Money;

  public constructor(cashDividendTransaction: CashDividendTransaction, income: number, incomeCurrency: string) {
    this.cashDividendTransaction = cashDividendTransaction;
    this.income = new Money(income, incomeCurrency);
  }

  public setIncome(income: Money) {
    this.income = income;
  }

  public getTotalProfit() {
    return this.income;
  }

  public getTotalIncome() {
    return this.getTotalProfit();
  }
}
