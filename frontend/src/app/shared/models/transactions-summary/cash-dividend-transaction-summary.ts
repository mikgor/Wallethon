import {CashDividendTransaction} from '../../../main/components/dashboard/models/CashDividendTransaction';

export class CashDividendTransactionSummary {
  cashDividendTransaction: CashDividendTransaction;
  income: number;

  public constructor(cashDividendTransaction: CashDividendTransaction, income: number) {
    this.cashDividendTransaction = cashDividendTransaction;
    this.income = income;
  }

  public setIncome(income: number) {
    this.income = income;
  }

  public getTotalProfit() {
    return this.income;
  }

  public getTotalIncome() {
    return this.getTotalProfit();
  }
}
