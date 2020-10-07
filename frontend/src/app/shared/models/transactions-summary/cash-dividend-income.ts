import {CashDividendTransaction} from '../../../main/components/dashboard/models/CashDividendTransaction';

export class CashDividendIncome {
  cashDividendTransaction: CashDividendTransaction;
  cashDividendRevenue: number;
  cashDividendOutcome: number;

  public constructor(cashDividendTransaction: CashDividendTransaction) {
    this.cashDividendTransaction = Object.assign({}, cashDividendTransaction);
    this.cashDividendRevenue = 0.00;
    this.cashDividendOutcome = 0.00;
  }

  public updateCashDividendOutcome(val: number) {
    this.cashDividendOutcome = val;
  }

  public addToCashDividendRevenue(val: number) {
    this.cashDividendRevenue += val;
  }

  public cashDividendIncome() {
    return this.cashDividendOutcome - this.cashDividendRevenue;
  }
}
