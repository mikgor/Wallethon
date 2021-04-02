import {CompanyStock} from '../../../main/components/dashboard/models/CompanyStock';
import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {StockSplitTransaction} from '../../../main/components/dashboard/models/StockSplitTransaction';
import {StockDividendTransaction} from '../../../main/components/dashboard/models/StockDividendTransaction';
import {SellStockTransactionSummary} from './sell-stock-transaction-summary';
import {CashDividendTransactionSummary} from './cash-dividend-transaction-summary';

export class StockSummary {
  companyStock: CompanyStock;
  buyStockTransactions: StockTransaction[];
  sellStockTransactionsSummaries: SellStockTransactionSummary[];
  stockSplitTransactions: StockSplitTransaction[];
  stockDividendTransactions: StockDividendTransaction[];
  cashDividendTransactionsSummaries: CashDividendTransactionSummary[];
  cashDividendTotal: number;
  stockDividendTotal: number;
  remainingStockQuantity: number;

  constructor(companyStock: CompanyStock, buyStockTransactions: StockTransaction[],
              sellStockTransactionsSummaries: SellStockTransactionSummary[],
              stockSplitTransactions: StockSplitTransaction[],
              stockDividendTransactions: StockDividendTransaction[],
              cashDividendTransactionsSummaries: CashDividendTransactionSummary[], cashDividendTotal: number,
              stockDividendTotal: number, remainingStockQuantity: number) {
    this.companyStock = companyStock;
    this.buyStockTransactions = buyStockTransactions;
    this.sellStockTransactionsSummaries = sellStockTransactionsSummaries;
    this.stockSplitTransactions = stockSplitTransactions;
    this.stockDividendTransactions = stockDividendTransactions;
    this.cashDividendTransactionsSummaries = cashDividendTransactionsSummaries;
    this.cashDividendTotal = cashDividendTotal;
    this.stockDividendTotal = stockDividendTotal;
    this.remainingStockQuantity = remainingStockQuantity;
  }

  public getSellStockTransactionsProfit() {
    let profit = 0;
    this.sellStockTransactionsSummaries.forEach(x => profit += x.getTotalProfit());
    return profit;
  }

  public getCashDividendTransactionsProfit() {
    let profit = 0;
    this.cashDividendTransactionsSummaries.forEach(x => profit += x.getTotalProfit());
    return profit;
  }

  public getTotalProfit() {
    return this.getSellStockTransactionsProfit() + this.getCashDividendTransactionsProfit();
  }

  public getSellStockTransactionsLoss() {
    let loss = 0;
    this.sellStockTransactionsSummaries.forEach(x => loss += x.getTotalLoss());
    return loss;
  }

  public getCashDividendTransactionsLoss() {
    return 0;
  }

  public getTotalLoss() {
    return this.getSellStockTransactionsLoss() + this.getCashDividendTransactionsLoss();
  }

  public getSellStockTransactionsCosts() {
    let costs = 0;
    this.sellStockTransactionsSummaries.forEach(x => costs += x.getTotalCosts());
    return costs;
  }

  public getCashDividendTransactionsCosts() {
    return 0;
  }

  public getTotalCosts() {
    return this.getSellStockTransactionsCosts() + this.getCashDividendTransactionsCosts();
  }

  public getSellStockTransactionsIncome() {
    let income = 0;
    this.sellStockTransactionsSummaries.forEach(x => income += x.getTotalIncome());
    return income;
  }

  public getCashDividendTransactionsIncome() {
    let income = 0;
    this.cashDividendTransactionsSummaries.forEach(x => income += x.getTotalIncome());
    return income;
  }

  public getTotalIncome() {
    return this.getSellStockTransactionsIncome() + this.getCashDividendTransactionsIncome();
  }

  public getBuyTransactionsCount() {
    return this.buyStockTransactions.length;
  }

  public getSellTransactionsCount() {
    return this.sellStockTransactionsSummaries.length;
  }

  public getSplitTransactionsCount() {
    return this.stockSplitTransactions.length;
  }

  public getCashDividendTransactionsCount() {
    return this.cashDividendTransactionsSummaries.length;
  }

  public getStockDividendTransactionsCount() {
    return this.stockDividendTransactions.length;
  }

  public getTotalBoughtQuantity() {
    let bought = 0;
    this.buyStockTransactions.forEach(transaction => bought += transaction.stockQuantity);
    return bought;
  }

  public getTotalSoldQuantity() {
    let sold = 0;
    this.sellStockTransactionsSummaries.forEach(transaction => sold += transaction.sellStockTransaction.stockQuantity);
    return sold;
  }
}
