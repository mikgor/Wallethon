import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {StockDividendTransaction} from '../../../main/components/dashboard/models/StockDividendTransaction';
import {StockSplitTransaction} from '../../../main/components/dashboard/models/StockSplitTransaction';
import {STOCK_FRACTION_DIGITS} from "../../../config";

export class ExtendedTransaction {
  transaction: StockTransaction|StockDividendTransaction;
  remainingQuantity: number;

  public constructor(transaction) {
    this.transaction = Object.assign({}, transaction);
    this.remainingQuantity = this.transaction.stockQuantity;
  }

  public updateRemainingQuantity(quantity: number) {
    this.remainingQuantity += Number(quantity.toPrecision(STOCK_FRACTION_DIGITS));
  }

  public splitTransaction(stockSplitTransaction: StockSplitTransaction) {
    if (this.remainingQuantity > 0) {
      this.remainingQuantity = (this.remainingQuantity * stockSplitTransaction.exchangeRatioFor) /
        stockSplitTransaction.exchangeRatioFrom;
      this.transaction.stockQuantity = (this.transaction.stockQuantity * stockSplitTransaction.exchangeRatioFor) /
        stockSplitTransaction.exchangeRatioFrom;
      if (!(this.transaction instanceof StockDividendTransaction)) {
        this.transaction.perStockPrice = (this.transaction.perStockPrice * stockSplitTransaction.exchangeRatioFrom) /
          stockSplitTransaction.exchangeRatioFor;
      }
    }
  }

  public getRemainingTotalValue() {
    let totalValue = 0.00;
    const transaction = this.transaction;
    if (!(transaction instanceof StockDividendTransaction)) {
      const stockQuantity = transaction.stockQuantity - this.remainingQuantity;
      const remainingRatio = stockQuantity / transaction.stockQuantity;
      const remainingCommission = transaction.commission * remainingRatio;
      const remainingTax = transaction.tax * remainingRatio;
      totalValue = (stockQuantity * transaction.perStockPrice) + remainingTax + remainingCommission;
    }
    return totalValue;
  }
}
