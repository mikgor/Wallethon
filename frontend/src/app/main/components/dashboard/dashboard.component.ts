import { Component, OnInit } from '@angular/core';
import {DashboardService} from './services/dashboard.service';
import {StockTransaction} from './models/StockTransaction';
import {DateTimeService} from '../../../shared/services/date-time.service';
import {StockSplitTransaction} from './models/StockSplitTransaction';
import {StockDividendTransaction} from './models/StockDividendTransaction';
import { CashDividendTransaction } from './models/CashDividendTransaction';
import {MoneyService} from '../../../shared/services/money.service';
import {TransactionsSummaryService} from '../../../shared/services/transactions-summary.service';
import {BrokerSummary} from '../../../shared/models/transactions-summary/broker-summary';

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
  transactions = [];
  summaries: BrokerSummary[];
  dataLoaded = false;

  public moneyService = MoneyService;

  constructor(public dashboardService: DashboardService,
              private dateTimeService: DateTimeService,
              public transactionsSummaryService: TransactionsSummaryService,
              ) { }

  ngOnInit(): void {
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

  private dataOnLoad() {
    if (this.stockTransactions && this.stockSplitTransactions && this.cashDividendTransactions &&
        this.stockDividendTransactions) {
      this.transactions = this.transactions.concat(this.stockTransactions);
      this.transactions = this.transactions.concat(this.stockSplitTransactions);
      this.transactions = this.transactions.concat(this.cashDividendTransactions);
      this.transactions = this.transactions.concat(this.stockDividendTransactions);
      this.summaries = this.transactionsSummaryService.getSummaries(this.transactions);
      this.transactions.sort(this.dateTimeService.sortByDateDesc);
      this.dataLoaded = true;
    }
  }
}
