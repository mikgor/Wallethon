import {UserBroker} from '../../main/components/dashboard/models/UserBroker';
import {Injectable} from '@angular/core';
import {StockTransaction} from '../../main/components/dashboard/models/StockTransaction';
import {StockSplitTransaction} from '../../main/components/dashboard/models/StockSplitTransaction';
import {CashDividendTransaction} from '../../main/components/dashboard/models/CashDividendTransaction';
import {StockDividendTransaction} from '../../main/components/dashboard/models/StockDividendTransaction';
import {DateTimeService} from './date-time.service';
import {StockSummary} from '../models/transactions-summary/stock-summary';
import {BrokerSummary} from '../models/transactions-summary/broker-summary';

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
    let preparedTransactions = [...transactions].sort(this.dateTimeService.sortByDateAsc);
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
