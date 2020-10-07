import {UserBroker} from '../../main/components/dashboard/models/UserBroker';
import {Injectable} from '@angular/core';
import {StockTransaction} from '../../main/components/dashboard/models/StockTransaction';
import {StockSplitTransaction} from '../../main/components/dashboard/models/StockSplitTransaction';
import {CashDividendTransaction} from '../../main/components/dashboard/models/CashDividendTransaction';
import {StockDividendTransaction} from '../../main/components/dashboard/models/StockDividendTransaction';
import {DateTimeService} from './date-time.service';
import {StockSummary} from '../models/transactions-summary/stock-summary';
import {BrokerSummary} from '../models/transactions-summary/broker-summary';
import {MoneyService} from './money.service';
import {StockIncomeSummary} from "../models/transactions-summary/stock-income-summary";
import {BrokersTotalIncomeSummary} from "../models/transactions-summary/brokers-total-income-summary";
import {CashDividendIncome} from "../models/transactions-summary/cash-dividend-income";

@Injectable({
  providedIn: 'root',
})

export class TransactionsSummaryService {
  brokersSummaries: BrokerSummary[];

  constructor(private dateTimeService: DateTimeService, private moneyService: MoneyService) {
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

  public calculateCashDividendTransactionIncome(cashDividendIncome: CashDividendIncome, currency: string) {
    const cashDividendTransaction = cashDividendIncome.cashDividendTransaction;
    this.moneyService.getExchangedValue(cashDividendTransaction.totalValue,
      cashDividendTransaction.date, cashDividendTransaction.totalValueCurrency, currency).subscribe(response =>
            cashDividendIncome.updateCashDividendOutcome(response));
  }

  public calculateStockIncomeSummaryIncome(stockIncomeSummary: StockIncomeSummary, currency: string) {
    const sellTransaction = stockIncomeSummary.sellTransaction;
    this.moneyService.getExchangedValue(sellTransaction.totalValue,
      sellTransaction.date, sellTransaction.totalValueCurrency, currency).subscribe(response =>
            stockIncomeSummary.updateOutcome(-response));

    for (const extendedTransaction of stockIncomeSummary.extendedTransactions) {
      const extendedTransactionValue = extendedTransaction.getRemainingTotalValue();
      if (!(extendedTransaction.transaction instanceof StockDividendTransaction)) {
        this.moneyService.getExchangedValue(extendedTransactionValue, extendedTransaction.transaction.date,
          extendedTransaction.transaction.totalValueCurrency, currency).subscribe(response =>
          stockIncomeSummary.addToRevenue(response));
      }
    }
  }

  public getIncomeAndTax(currency: string, tax: number) {
    const brokerIncomeSummaries = [];
    for (const brokerSummary of this.brokersSummaries) {
      const brokerIncomeSummary = brokerSummary.getIncomeData();
      for (const stockIncomeSummary of brokerIncomeSummary.stockIncomeSummaries) {
        this.calculateStockIncomeSummaryIncome(stockIncomeSummary, currency);
      }
      for (const cashDividendIncomeTransaction of brokerIncomeSummary.cashDividendIncomeTransactions) {
        this.calculateCashDividendTransactionIncome(cashDividendIncomeTransaction, currency);
      }
      brokerIncomeSummaries.push(brokerIncomeSummary);
    }
    return new BrokersTotalIncomeSummary(tax, brokerIncomeSummaries);
  }
}
