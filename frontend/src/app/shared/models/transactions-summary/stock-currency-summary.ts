import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {CashDividendTransaction} from '../../../main/components/dashboard/models/CashDividendTransaction';

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
      this.boughtMoney += stockTransaction.totalValue;
    }
    if (stockTransaction.type === 'SELL') {
      this.soldMoney += stockTransaction.totalValue;
    }
  }

  public calculateCashDividendTransaction(cashDividendTransaction: CashDividendTransaction) {
    this.dividend += cashDividendTransaction.totalValue;
  }
}
