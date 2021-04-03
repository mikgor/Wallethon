import { Component, OnInit } from '@angular/core';
import {DashboardService} from './services/dashboard.service';
import {StockTransaction} from './models/StockTransaction';
import {DateTimeService} from '../../../shared/services/date-time.service';
import {StockSplitTransaction} from './models/StockSplitTransaction';
import {StockDividendTransaction} from './models/StockDividendTransaction';
import { CashDividendTransaction } from './models/CashDividendTransaction';
import {MoneyService} from '../../../shared/services/money.service';
import { APP_ROUTES } from 'src/app/routes-config';
import {UserBrokerStockSummary} from '../../../shared/models/transactions-summary/user-broker-stock-summary';
import {UserBroker} from './models/UserBroker';
import {AutoCompleteFilter} from '../../../shared/models/auto-complete-filter';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  stockTransactions: StockTransaction[];
  buyStockTransactionsCounter = 0;
  sellStockTransactionsCounter = 0;
  stockSplitTransactions: StockSplitTransaction[];
  cashDividendTransactions: CashDividendTransaction[];
  stockDividendTransactions: StockDividendTransaction[];
  userBrokers: UserBroker[];
  transactions = [];
  showIncomeAndTax = false;
  dataLoaded = false;
  incomeAndTaxDataLoaded = false;
  MoneyService = MoneyService;
  userBrokerStockSummaries: UserBrokerStockSummary[] = [];
  APP_ROUTES = APP_ROUTES;
  dateFrom;
  dateTo;
  taxRate = 0.19;
  cashDividendTaxRate = 0.00;
  incomeAndTaxCurrency = 'PLN';
  dateFromSelected;
  dateToSelected;
  taxRateSelected;
  cashDividendTaxRateSelected;
  incomeAndTaxCurrencySelected;
  currenciesAutoCompleteFilter: AutoCompleteFilter;

  constructor(public dashboardService: DashboardService,
              private dateTimeService: DateTimeService,
              private moneyService: MoneyService,
              ) { }

  ngOnInit(): void {
    const previousYear = new Date().getFullYear() - 1;
    this.dateFrom = new Date(previousYear, 0, 1, 0, 0, 0);
    this.dateTo = new Date(previousYear, 11, 31, 23, 59, 59);
    this.dateFromSelected = this.dateFrom;
    this.dateToSelected = this.dateTo;
    this.taxRateSelected = this.taxRate;
    this.cashDividendTaxRateSelected = this.cashDividendTaxRate;
    this.incomeAndTaxCurrencySelected = this.incomeAndTaxCurrency;
    this.currenciesAutoCompleteFilter = new AutoCompleteFilter('symbol', {1: 'startswith'},
      this.moneyService.getExchangeCurrencies.bind(this.moneyService), true);

    this.dashboardService.getStockTransactions().subscribe(stockTransactions =>
        this.stockTransactionsLoaded(stockTransactions)
    );
    this.dashboardService.getStockSplitTransactions().subscribe(stockSplitTransactions =>
        this.stockSplitTransactionsLoaded(stockSplitTransactions)
    );
    this.dashboardService.getCashDividendTransactions().subscribe(cashDividendTransactions =>
        this.cashDividendTransactionsLoaded(cashDividendTransactions)
    );
    this.dashboardService.getStockDividendTransactions().subscribe(stockDividendTransactions =>
        this.stockDividendTransactionsLoaded(stockDividendTransactions)
    );
    this.dashboardService.getUserBrokers().subscribe(userBrokers =>
        this.userBrokersLoaded(userBrokers)
    );
  }

  private stockTransactionsLoaded(stockTransactions) {
    this.stockTransactions = stockTransactions;
    this.buyStockTransactionsCounter = this.stockTransactions.filter(t => t.type === 'BUY').length;
    this.sellStockTransactionsCounter = this.stockTransactions.length - this.buyStockTransactionsCounter;
    this.dataOnLoad();
  }

  private stockSplitTransactionsLoaded(stockSplitTransactions) {
    this.stockSplitTransactions = stockSplitTransactions;
    this.dataOnLoad();
  }

  private cashDividendTransactionsLoaded(cashDividendTransactions) {
    this.cashDividendTransactions = cashDividendTransactions;
    this.dataOnLoad();
  }

  private stockDividendTransactionsLoaded(stockDividendTransactions) {
    this.stockDividendTransactions = stockDividendTransactions;
    this.dataOnLoad();
  }

  private userBrokerStockSummaryLoaded(userBrokerStockSummary) {
    this.userBrokerStockSummaries.push(userBrokerStockSummary);
  }

  private userBrokersLoaded(userBrokers) {
    this.userBrokers = userBrokers;
    for (const userBroker of this.userBrokers) {
      this.dashboardService.getTransactionsSummary(userBroker.id, this.dateFrom, this.dateTo).
      subscribe(transactionsSummary =>
        this.userBrokerStockSummaryLoaded(transactionsSummary)
      );
    }
    this.dataOnLoad();
  }

  private dataOnLoad() {
    if (this.stockTransactions && this.stockSplitTransactions && this.cashDividendTransactions &&
        this.stockDividendTransactions && this.userBrokerStockSummaries) {
      this.transactions = this.transactions.concat(this.stockTransactions);
      this.transactions = this.transactions.concat(this.stockSplitTransactions);
      this.transactions = this.transactions.concat(this.cashDividendTransactions);
      this.transactions = this.transactions.concat(this.stockDividendTransactions);
      this.transactions.sort(this.dateTimeService.sortByDateDesc);
      this.dataLoaded = true;
    }
  }

  public showIncomeAndTaxData() {
    this.showIncomeAndTax = !this.showIncomeAndTax;
    if (this.taxRateSelected !== this.taxRate || this.cashDividendTaxRateSelected !== this.cashDividendTaxRate
        || this.incomeAndTaxCurrencySelected !== this.incomeAndTaxCurrency) {
      this.taxRateSelected = this.taxRate;
      this.cashDividendTaxRateSelected = this.cashDividendTaxRate;
      this.incomeAndTaxCurrencySelected = this.incomeAndTaxCurrency;
      this.incomeAndTaxDataLoaded = false;
      this.showIncomeAndTax = true;
    }
    if (this.showIncomeAndTax && !this.incomeAndTaxDataLoaded) {
      for (const userBrokerStockSummary of this.userBrokerStockSummaries) {
        this.dashboardService.calculateProfitFromUserBrokerStockSummary(userBrokerStockSummary, this.incomeAndTaxCurrency);
      }
      this.incomeAndTaxDataLoaded = true;
    }
  }

  public dateRangeChanged() {
    if (this.dateTo < this.dateFrom) {
      const dateToC = this.dateTo;
      this.dateTo = this.dateFrom;
      this.dateFrom = dateToC;
    }
    this.dateFromSelected = this.dateFrom;
    this.dateToSelected = this.dateTo;

    this.showIncomeAndTax = false;
    this.incomeAndTaxDataLoaded = false;
    this.userBrokerStockSummaries = [];

    for (const userBroker of this.userBrokers) {
      this.dashboardService.getTransactionsSummary(userBroker.id, this.dateFrom, this.dateTo).
        subscribe(transactionsSummary =>
          this.userBrokerStockSummaryLoaded(transactionsSummary)
        );
    }
  }
}
