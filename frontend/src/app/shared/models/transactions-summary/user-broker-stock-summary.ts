import {UserBroker} from '../../../main/components/dashboard/models/UserBroker';
import {StockSummary} from './stock-summary';
import {Money} from "../money";

export class UserBrokerStockSummary {
  id: string;
  dateFrom: Date;
  dateTo: Date;
  userBroker: UserBroker;
  stockSummaries: StockSummary[];

  public constructor(id: string, dateFrom: Date, dateTo: Date, userBroker: UserBroker, stockSummaries: StockSummary[]) {
    this.id = id;
    this.dateFrom = dateFrom;
    this.dateTo = dateTo;
    this.userBroker = userBroker;
    this.stockSummaries = stockSummaries;
  }

  public getSellStockTransactionsProfit() {
    let profit = new Money(0);
    this.stockSummaries.forEach(x => profit = profit.sum(x.getSellStockTransactionsProfit()));
    return profit;
  }

  public getCashDividendTransactionsProfit() {
    let profit = new Money(0);
    this.stockSummaries.forEach(x => profit = profit.sum(x.getCashDividendTransactionsProfit()));
    return profit;
  }

  public getTotalProfit() {
    return this.getSellStockTransactionsProfit().sum(this.getCashDividendTransactionsProfit());
  }

  public getSellStockTransactionsLoss() {
    let loss = new Money(0);
    this.stockSummaries.forEach(x => loss = loss.sum(x.getSellStockTransactionsLoss()));
    return loss;
  }
  public getCashDividendTransactionsLoss() {
    let loss = new Money(0);
    this.stockSummaries.forEach(x => loss = loss.sum(x.getCashDividendTransactionsLoss()));
    return loss;
  }

  public getTotalLoss() {
    return this.getSellStockTransactionsLoss().sum(this.getCashDividendTransactionsLoss());
  }

  public getSellStockTransactionsCosts() {
    let costs = new Money(0);
    this.stockSummaries.forEach(x => costs = costs.sum(x.getSellStockTransactionsCosts()));
    return costs;
  }

  public getCashDividendTransactionsCosts() {
    let costs = new Money(0);
    this.stockSummaries.forEach(x => costs = costs.sum(x.getCashDividendTransactionsCosts()));
    return costs;
  }

  public getTotalCosts() {
    return this.getSellStockTransactionsCosts().sum(this.getCashDividendTransactionsCosts());
  }

  public getSellStockTransactionsIncome() {
    let income = new Money(0);
    this.stockSummaries.forEach(x => income = income.sum(x.getSellStockTransactionsIncome()));
    return income;
  }

  public getCashDividendTransactionsIncome() {
    let income = new Money(0);
    this.stockSummaries.forEach(x => income = income.sum(x.getCashDividendTransactionsIncome()));
    return income;
  }

  public getTotalIncome() {
    return this.getSellStockTransactionsIncome().sum(this.getCashDividendTransactionsIncome());
  }

  public getSellStockTransactionsProfitTax(taxRate: number) {
    return this.getSellStockTransactionsProfit().multiply(taxRate);
  }

  public getCashDividendTransactionsProfitTax(cashDividendTaxRate: number) {
    return this.getCashDividendTransactionsProfit().multiply(cashDividendTaxRate);
  }

  public getTotalProfitTax(taxRate: number, cashDividendTaxRate: number) {
    return this.getSellStockTransactionsProfitTax(taxRate)
      .sum(this.getCashDividendTransactionsProfitTax(cashDividendTaxRate));
  }
}
