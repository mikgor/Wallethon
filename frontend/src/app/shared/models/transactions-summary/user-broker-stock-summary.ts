import {UserBroker} from '../../../main/components/dashboard/models/UserBroker';
import {StockSummary} from './stock-summary';

export class UserBrokerStockSummary {
  id: string;
  dateFrom: Date;
  dateTo: Date;
  userBroker: UserBroker;
  currency: string;
  stockSummaries: StockSummary[];

  public constructor(id: string, dateFrom: Date, dateTo: Date, userBroker: UserBroker,
                     currency: string, stockSummaries: StockSummary[]) {
    this.id = id;
    this.dateFrom = dateFrom;
    this.dateTo = dateTo;
    this.userBroker = userBroker;
    this.currency = currency;
    this.stockSummaries = stockSummaries;
  }

  public getSellStockTransactionsProfit() {
    let profit = 0;
    this.stockSummaries.forEach(x => profit += x.getSellStockTransactionsProfit());
    return profit;
  }

  public getCashDividendTransactionsProfit() {
    let profit = 0;
    this.stockSummaries.forEach(x => profit += x.getCashDividendTransactionsProfit());
    return profit;
  }

  public getTotalProfit() {
    return this.getSellStockTransactionsProfit() + this.getCashDividendTransactionsProfit();
  }

  public getSellStockTransactionsLoss() {
    let loss = 0;
    this.stockSummaries.forEach(x => loss += x.getSellStockTransactionsLoss());
    return loss;
  }

  public getCashDividendTransactionsLoss() {
    let loss = 0;
    this.stockSummaries.forEach(x => loss += x.getCashDividendTransactionsLoss());
    return loss;
  }

  public getTotalLoss() {
    return this.getSellStockTransactionsLoss() + this.getCashDividendTransactionsLoss();
  }

  public getSellStockTransactionsCosts() {
    let costs = 0;
    this.stockSummaries.forEach(x => costs += x.getSellStockTransactionsCosts());
    return costs;
  }

  public getCashDividendTransactionsCosts() {
    let costs = 0;
    this.stockSummaries.forEach(x => costs += x.getCashDividendTransactionsCosts());
    return costs;
  }

  public getTotalCosts() {
    return this.getSellStockTransactionsCosts() + this.getCashDividendTransactionsCosts();
  }

  public getSellStockTransactionsIncome() {
    let income = 0;
    this.stockSummaries.forEach(x => income += x.getSellStockTransactionsIncome());
    return income;
  }

  public getCashDividendTransactionsIncome() {
    let income = 0;
    this.stockSummaries.forEach(x => income += x.getCashDividendTransactionsIncome());
    return income;
  }

  public getTotalIncome() {
    return this.getSellStockTransactionsIncome() + this.getCashDividendTransactionsIncome();
  }

  public getTotalProfitTax(taxRate: number) {
    return this.getTotalProfit() * taxRate;
  }
}
