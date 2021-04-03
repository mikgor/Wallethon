import {CompanyStock} from '../../../main/components/dashboard/models/CompanyStock';
import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {StockSplitTransaction} from '../../../main/components/dashboard/models/StockSplitTransaction';
import {StockDividendTransaction} from '../../../main/components/dashboard/models/StockDividendTransaction';
import {SellStockTransactionSummary} from './sell-stock-transaction-summary';
import {CashDividendTransactionSummary} from './cash-dividend-transaction-summary';
import {Money} from "../money";

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
    let profit = new Money(0);
    this.sellStockTransactionsSummaries.forEach(x => profit = profit.sum(x.getTotalProfit()));
    return profit;
  }

  public getCashDividendTransactionsProfit() {
    let profit = new Money(0);
    this.cashDividendTransactionsSummaries.forEach(x => profit = profit.sum(x.getTotalProfit()));
    return profit;
  }

  public getTotalProfit() {
    return this.getSellStockTransactionsProfit().sum(this.getCashDividendTransactionsProfit());
  }

  public getSellStockTransactionsLoss() {
    let loss = new Money(0);
    this.sellStockTransactionsSummaries.forEach(x => loss = loss.sum(x.getTotalLoss()));
    return loss;
  }

  public getCashDividendTransactionsLoss() {
    return new Money(0);
  }

  public getTotalLoss() {
    return this.getSellStockTransactionsLoss().sum(this.getCashDividendTransactionsLoss());
  }

  public getSellStockTransactionsCosts() {
    let costs = new Money(0);
    this.sellStockTransactionsSummaries.forEach(x => costs = costs.sum(x.getTotalCosts()));
    return costs;
  }

  public getCashDividendTransactionsCosts() {
    return new Money(0);
  }

  public getTotalCosts() {
    return this.getSellStockTransactionsCosts().sum(this.getCashDividendTransactionsCosts());
  }

  public getSellStockTransactionsIncome() {
    let income = new Money(0);
    this.sellStockTransactionsSummaries.forEach(x => income = income.sum(x.getTotalIncome()));
    return income;
  }

  public getCashDividendTransactionsIncome() {
    let income = new Money(0);
    this.cashDividendTransactionsSummaries.forEach(x => income = income.sum(x.getTotalIncome()));
    return income;
  }

  public getTotalIncome() {
    return this.getSellStockTransactionsIncome().sum(this.getCashDividendTransactionsIncome());
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
