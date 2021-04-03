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

  public getProfit() {
    const profit = this.income.subtract(this.costs);
    return profit.amount > 0 ? profit : new Money(0, this.income.currency);
  }

  public getLoss() {
    const loss = this.income.subtract(this.costs);
    return loss.amount < 0 ? loss : new Money(0, this.income.currency);
  }

  public getTotalProfitOrLoss() {
    return this.getProfit().amount === 0 ? this.getLoss() : this.getProfit();
  }

  public getAdditionalCosts(sellStockTransaction: StockTransaction) {
    const commissionsSum = sellStockTransaction.commission.sum(sellStockTransaction.tax);
    return commissionsSum.multiply(this.originQuantitySoldRatio);
  }

  public getTransactionDate() {
    return null;
  }
}
