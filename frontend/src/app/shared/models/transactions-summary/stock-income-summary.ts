import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {ExtendedTransaction} from './extended-transaction';

export class StockIncomeSummary {
  sellTransaction: StockTransaction;
  extendedTransactions: ExtendedTransaction[];
  revenue: number;
  outcome: number;

  public constructor(sellTransaction: StockTransaction) {
    this.sellTransaction = Object.assign({}, sellTransaction);
    this.extendedTransactions = [];
    this.revenue = 0.00;
    this.outcome = 0.00;
  }

  public addExtendedTransaction(extendedTansaction: ExtendedTransaction) {
    this.extendedTransactions.push(extendedTansaction);
  }

  public updateOutcome(val: number) {
    this.outcome = val;
  }

  public addToRevenue(val: number) {
    this.revenue += val;
  }

  public income() {
    return this.outcome - this.revenue;
  }
}
