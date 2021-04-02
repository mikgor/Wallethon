import {StockDividendTransaction} from '../../../main/components/dashboard/models/StockDividendTransaction';
import {SellRelatedTransaction} from './sell-related-transaction';

export class SellRelatedStockDividendTransaction extends SellRelatedTransaction {
  stockDividendTransaction: StockDividendTransaction;

  public constructor(stockDividendTransaction: StockDividendTransaction, soldQuantity: number, originQuantitySoldRatio: number,
                     costs: number, income: number, costsCurrency: string) {
    super(soldQuantity, originQuantitySoldRatio, costs, income, costsCurrency);
    this.stockDividendTransaction = stockDividendTransaction;
  }

  public getProfit() {
    return this.income;
  }

  public getTransactionDate() {
    return this.stockDividendTransaction.date;
  }
}
