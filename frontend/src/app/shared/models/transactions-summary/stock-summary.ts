import {CompanyStock} from '../../../main/components/dashboard/models/CompanyStock';
import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {StockSplitTransaction} from '../../../main/components/dashboard/models/StockSplitTransaction';
import {CashDividendTransaction} from '../../../main/components/dashboard/models/CashDividendTransaction';
import {StockDividendTransaction} from '../../../main/components/dashboard/models/StockDividendTransaction';
import {StockCurrencySummary} from './stock-currency-summary';

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
      (this.totalQuantity * stockSplitTransaction.exchangeRatioFor) / stockSplitTransaction.exchangeRatioFrom;
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
