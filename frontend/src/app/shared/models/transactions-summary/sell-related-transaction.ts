import {StockTransaction} from '../../../main/components/dashboard/models/StockTransaction';
import {Money} from '../money';

export class SellRelatedTransaction {
  soldQuantity: number;
  originQuantitySoldRatio: number;
  costs: Money;
  income: Money;

  public constructor(soldQuantity: number, originQuantitySoldRatio: number, costs: number, costsCurrency: string,
                     income: number, incomeCurrency: string) {
    this.soldQuantity = soldQuantity;
    this.originQuantitySoldRatio = originQuantitySoldRatio;
    this.costs = new Money(costs, costsCurrency);
    this.income = new Money(income, incomeCurrency);
  }

  public setCostsAndIncome(costs: Money, income: Money) {
    this.costs = costs;
    this.income = income;
  }

  public getProfitLoss() {
    const profitLoss = this.income.subtract(this.costs);
    return profitLoss;
  }

  public getAdditionalCosts(sellStockTransaction: StockTransaction) {
    const commissionsSum = sellStockTransaction.commission.sum(sellStockTransaction.tax);
    return commissionsSum.multiply(this.originQuantitySoldRatio);
  }

  public getTransactionDate() {
    return null;
  }
}
