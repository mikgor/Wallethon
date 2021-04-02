import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {SellRelatedTransaction} from './sell-related-transaction';

export class SellRelatedBuyStockTransaction extends SellRelatedTransaction {
  buyStockTransaction: StockTransaction;

  public constructor(buyStockTransaction: StockTransaction, soldQuantity: number, originQuantitySoldRatio: number,
                     costs: number, income: number, costsCurrency: string) {
    super(soldQuantity, originQuantitySoldRatio, costs, income, costsCurrency);
    this.buyStockTransaction = buyStockTransaction;
  }

  public getAdditionalCosts(sellStockTransaction: StockTransaction) {
    return this.originQuantitySoldRatio * this.buyStockTransaction.totalValue + super.getAdditionalCosts(sellStockTransaction);
  }

  public getTransactionDate() {
    return this.buyStockTransaction.date;
  }
}
