import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {SellRelatedBuyStockTransaction} from './sell-related-buy-stock-transaction';
import {SellRelatedStockDividendTransaction} from './sell-related-stock-dividend-transaction';
import {Money} from '../money';

export class SellStockTransactionSummary {
  sellStockTransaction: StockTransaction;
  sellRelatedBuyStockTransactions: SellRelatedBuyStockTransaction[];
  sellRelatedStockDividendTransactions: SellRelatedStockDividendTransaction[];

  public constructor(sellStockTransaction: StockTransaction,
                     sellRelatedBuyStockTransactions: SellRelatedBuyStockTransaction[],
                     sellRelatedStockDividendTransactions: SellRelatedStockDividendTransaction[]) {
    this.sellStockTransaction = sellStockTransaction;
    this.sellRelatedBuyStockTransactions = sellRelatedBuyStockTransactions;
    this.sellRelatedStockDividendTransactions = sellRelatedStockDividendTransactions;
  }

  public getTotalProfitLoss() {
    let profitLoss = new Money(0);
    this.sellRelatedBuyStockTransactions.forEach(x => profitLoss = profitLoss.sum(x.getProfitLoss()));
    this.sellRelatedStockDividendTransactions.forEach(x => profitLoss = profitLoss.sum(x.getProfitLoss()));
    return profitLoss;
  }


  public getTotalCosts() {
    let costs = new Money(0);
    this.sellRelatedBuyStockTransactions.forEach(x => costs = costs.sum(x.costs));
    this.sellRelatedStockDividendTransactions.forEach(x => costs = costs.sum(x.costs));
    return costs;
  }

  public getTotalIncome() {
    let income = new Money(0);
    this.sellRelatedBuyStockTransactions.forEach(x => income = income.sum(x.income));
    this.sellRelatedStockDividendTransactions.forEach(x => income = income.sum(x.income));
    return income;
  }
}
