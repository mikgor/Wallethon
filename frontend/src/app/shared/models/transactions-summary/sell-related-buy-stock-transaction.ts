import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {SellRelatedTransaction} from './sell-related-transaction';

export class SellRelatedBuyStockTransaction extends SellRelatedTransaction {
  buyStockTransaction: StockTransaction;

  public constructor(buyStockTransaction: StockTransaction, soldQuantity: number, originQuantitySoldRatio: number,
                     costs: number, costsCurrency: string, income: number, incomeCurrency: string) {
    super(soldQuantity, originQuantitySoldRatio, costs, costsCurrency, income, incomeCurrency);
    this.buyStockTransaction = buyStockTransaction;
  }

  public getAdditionalCosts(sellStockTransaction: StockTransaction) {
    const valueAndCommissionsSum = this.buyStockTransaction.totalValue.sum(super.getAdditionalCosts(sellStockTransaction));
    return valueAndCommissionsSum.multiply(this.originQuantitySoldRatio);
  }

  public getTransactionDate() {
    return this.buyStockTransaction.date;
  }
}
