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

  public getTotalProfit() {
    let profit = new Money(0);
    this.sellRelatedBuyStockTransactions.forEach(x => profit = profit.sum(x.getProfit()));
    this.sellRelatedStockDividendTransactions.forEach(x => profit = profit.sum(x.getProfit()));
    return profit;
  }

  public getTotalLoss() {
    let loss = new Money(0);
    this.sellRelatedBuyStockTransactions.forEach(x => loss = loss.sum(x.getLoss()));
    this.sellRelatedStockDividendTransactions.forEach(x => loss = loss.sum(x.getLoss()));
    return loss;
  }

  public getTotalProfitOrLoss() {
    return this.getTotalProfit().amount === 0 ? this.getTotalLoss() : this.getTotalProfit();
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
