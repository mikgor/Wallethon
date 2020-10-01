import {UserBroker} from '../../main/components/dashboard/models/UserBroker';
import {CompanyStock} from '../../main/components/dashboard/models/CompanyStock';

export class StockCurrencySummary {
  currency: string;
  boughtMoney: number;
  soldMoney: number;
  dividend: number;

  constructor(currency: string) {
    this.currency = currency;
    this.boughtMoney = 0.00;
    this.soldMoney = 0.00;
    this.dividend = 0.00;
  }

  public calculateStockTransaction(stockTransaction: StockTransaction) {
    if (stockTransaction.type === 'BUY') {
      this.boughtMoney += Number(stockTransaction.totalValue);
    }
    if (stockTransaction.type === 'SELL') {
      this.soldMoney += Number(stockTransaction.totalValue);
    }
  }

  public calculateCashDividendTransaction(cashDividendTransaction: CashDividendTransaction) {
    this.dividend += Number(cashDividendTransaction.totalValue);
  }
}

export class StockSummary {
  companyStock: CompanyStock;
  stockCurrencySummaries: StockCurrencySummary[];
  buyTransactionCounter: number;
  sellTransactionCounter: number;
  cashDividendCounter: number;
  stockDividendCounter: number;
  stockSplitCounter: number;
  boughtQuantity: number;
  soldQuantity: number;
  totalQuantity: number;

  constructor(companyStock: CompanyStock) {
    this.companyStock = companyStock;
    this.stockCurrencySummaries = [];
    this.buyTransactionCounter = 0;
    this.sellTransactionCounter = 0;
    this.cashDividendCounter = 0;
    this.stockDividendCounter = 0;
    this.stockSplitCounter = 0;
    this.boughtQuantity = 0.00;
    this.soldQuantity = 0.00;
    this.totalQuantity = 0.00;
  }

  private getStockCurrencySummary(currency: string) {
    let stockCurrencySummary: StockCurrencySummary = this.stockCurrencySummaries.filter(x => x.currency === currency)[0];
    if (stockCurrencySummary === undefined) {
      const newStockCurrencySummary = new StockCurrencySummary(currency);
      this.stockCurrencySummaries.push(newStockCurrencySummary);
      stockCurrencySummary = newStockCurrencySummary;
    }
    return stockCurrencySummary;
  }

  private getStockCurrencySummaryIndex(currency: string) {
    return this.stockCurrencySummaries.indexOf(this.getStockCurrencySummary(currency));
  }

  private updateStockCurrencySummary(stockCurrencySummary: StockCurrencySummary) {
    this.stockCurrencySummaries[this.getStockCurrencySummaryIndex(stockCurrencySummary.currency)] = stockCurrencySummary;
  }

  public calculateStockTransaction(stockTransaction: StockTransaction) {
    const stockCurrencySummary: StockCurrencySummary =
          this.getStockCurrencySummary(stockTransaction.totalValueCurrency);
    if (stockTransaction.type === 'BUY') {
      this.buyTransactionCounter += 1;
      this.boughtQuantity += stockTransaction.stockQuantity;
      this.totalQuantity += stockTransaction.stockQuantity;
    }
    if (stockTransaction.type === 'SELL') {
      this.sellTransactionCounter += 1;
      this.soldQuantity += stockTransaction.stockQuantity;
      this.totalQuantity -= stockTransaction.stockQuantity;
    }
    stockCurrencySummary.calculateStockTransaction(stockTransaction);
    this.updateStockCurrencySummary(stockCurrencySummary);
  }

  public calculateStockSplitTransaction(stockSplitTransaction: StockSplitTransaction) {
    this.stockSplitCounter += 1;
    this.totalQuantity =
      (this.totalQuantity * stockSplitTransaction.exchangeRatioFrom) / stockSplitTransaction.exchangeRatioFor;
  }

  public calculateCashDividendTransaction(cashDividendTransaction: CashDividendTransaction) {
    this.cashDividendCounter += 1;
    const stockCurrencySummary: StockCurrencySummary =
          this.getStockCurrencySummary(cashDividendTransaction.totalValueCurrency);
    stockCurrencySummary.calculateCashDividendTransaction(cashDividendTransaction);
    this.updateStockCurrencySummary(stockCurrencySummary);
  }

  public calculateStockDividendTransaction(stockDividendTransaction: StockDividendTransaction) {
    this.stockDividendCounter += 1;
    this.totalQuantity += Number(stockDividendTransaction.stockQuantity);
  }

  public getTotalQuantityText() {
    return 'Total quantity of stocks (including all buy and sell transactions '
      + '\nquantities, stock splits and stock dividends, calculated from beginning).'
      + `\nBought quantity: ${this.boughtQuantity}`
      + `\nSold quantity: ${this.soldQuantity}`;
  }
}

export class BrokerSummary {
  broker: UserBroker;
  stockSummaries: StockSummary[];

  constructor(broker: UserBroker) {
    this.broker = broker;
    this.stockSummaries = [];
  }

  public getStockSummary(companyStock: CompanyStock) {
    let stockSummary: StockSummary = this.stockSummaries.filter(x => x.companyStock.id === companyStock.id)[0];
    if (stockSummary === undefined) {
      const newStockSummary = new StockSummary(companyStock);
      this.stockSummaries.push(newStockSummary);
      stockSummary = newStockSummary;
    }
    return stockSummary;
  }

  private getStockSummaryIndex(companyStock: CompanyStock) {
    return this.stockSummaries.indexOf(this.getStockSummary(companyStock));
  }

  private updateStockSummary(stockSummary: StockSummary) {
    this.stockSummaries[this.getStockSummaryIndex(stockSummary.companyStock)] = stockSummary;
  }

  public calculateStockSplitTransaction(stockSplitTransaction: StockSplitTransaction) {
    const stockSummary: StockSummary = this.getStockSummary(stockSplitTransaction.companyStock);
    stockSummary.calculateStockSplitTransaction(stockSplitTransaction);
    this.updateStockSummary(stockSummary);
  }
}

import {Injectable} from '@angular/core';
import {StockTransaction} from '../../main/components/dashboard/models/StockTransaction';
import {StockSplitTransaction} from '../../main/components/dashboard/models/StockSplitTransaction';
import {CashDividendTransaction} from '../../main/components/dashboard/models/CashDividendTransaction';
import {StockDividendTransaction} from '../../main/components/dashboard/models/StockDividendTransaction';
import {DateTimeService} from './date-time.service';

@Injectable({
  providedIn: 'root',
})

export class TransactionsSummaryService {
  brokersSummaries: BrokerSummary[];

  constructor(private dateTimeService: DateTimeService) {
    this.brokersSummaries = [];
  }

  public getTransactionType(transaction) {
    return transaction.constructor.name;
  }

  private getBrokerSummary(broker: UserBroker) {
    let brokerSummary: BrokerSummary = this.brokersSummaries.filter(x => x.broker.id === broker.id)[0];
    if (brokerSummary === undefined) {
      const newBrokerSummary = new BrokerSummary(broker);
      this.brokersSummaries.push(newBrokerSummary);
      brokerSummary = newBrokerSummary;
    }
    return brokerSummary;
  }

  private getBrokerSummaryIndex(broker: UserBroker) {
    return this.brokersSummaries.indexOf(this.getBrokerSummary(broker));
  }

  private updateBrokerSummary(brokerSummary: BrokerSummary) {
    this.brokersSummaries[this.getBrokerSummaryIndex(brokerSummary.broker)] = brokerSummary;
  }

  private calculateStockSplitTransaction(stockSplitTransaction: StockSplitTransaction) {
    for (const broker of this.brokersSummaries) {
      broker.calculateStockSplitTransaction(stockSplitTransaction);
      this.updateBrokerSummary(broker);
    }
  }

  public getSummaries(transactions, toDate: Date = null) {
    let preparedTransactions = transactions.sort(this.dateTimeService.sortByDateAsc);
    if (toDate) {
      preparedTransactions = preparedTransactions.filter(t => t.date.getTime() <= toDate.getTime());
    }
    for (const transaction of preparedTransactions) {
      if (transaction.broker?.id === undefined) { // StockSplitTransaction
        this.calculateStockSplitTransaction(transaction);
        continue;
      }
      const brokerSummary: BrokerSummary = this.getBrokerSummary(transaction.broker);
      const stockSummary: StockSummary = brokerSummary.getStockSummary(transaction.companyStock);
      switch (this.getTransactionType(transaction)) {
        case 'StockTransaction':
          stockSummary.calculateStockTransaction(transaction);
          break;
        case 'CashDividendTransaction':
          stockSummary.calculateCashDividendTransaction(transaction);
          break;
        case 'StockDividendTransaction':
          stockSummary.calculateStockDividendTransaction(transaction);
          break;
      }
      this.updateBrokerSummary(brokerSummary);
    }
    return this.brokersSummaries;
  }


}
