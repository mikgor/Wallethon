import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {SellRelatedBuyStockTransaction} from './sell-related-buy-stock-transaction';
import {SellRelatedStockDividendTransaction} from './sell-related-stock-dividend-transaction';

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
    let profit = 0;
    this.sellRelatedBuyStockTransactions.forEach(x => profit += x.getProfit());
    this.sellRelatedStockDividendTransactions.forEach(x => profit += x.getProfit());
    return profit;
  }

  public getTotalLoss() {
    let loss = 0;
    this.sellRelatedBuyStockTransactions.forEach(x => loss += x.getLoss());
    this.sellRelatedStockDividendTransactions.forEach(x => loss += x.getLoss());
    return loss;
  }

  public getTotalCosts() {
    let costs = 0;
    this.sellRelatedBuyStockTransactions.forEach(x => costs += x.costs);
    this.sellRelatedStockDividendTransactions.forEach(x => costs += x.costs);
    return costs;
  }

  public getTotalIncome() {
    let income = 0;
    this.sellRelatedBuyStockTransactions.forEach(x => income += x.income);
    this.sellRelatedStockDividendTransactions.forEach(x => income += x.income);
    return income;
  }
}
