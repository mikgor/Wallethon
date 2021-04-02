import {StockTransaction} from "../../../main/components/dashboard/models/StockTransaction";

export class SellRelatedTransaction {
  soldQuantity: number;
  originQuantitySoldRatio: number;
  costs: number;
  costsCurrency: string;
  income: number;

  public constructor(soldQuantity: number, originQuantitySoldRatio: number, costs: number,
                     income: number, costsCurrency: string) {
    this.soldQuantity = soldQuantity;
    this.originQuantitySoldRatio = originQuantitySoldRatio;
    this.costsCurrency = costsCurrency;
    this.costs = costs;
    this.income = income;
  }

  public currencyEquals(currency: string) {
    return currency === this.costsCurrency;
  }

  public setCostsAndIncome(costs: number, income: number) {
    this.costs = costs;
    this.income = income;
  }

  public getProfit() {
    const profit = this.income - this.costs;
    return profit > 0 ? profit : 0;
  }

  public getLoss() {
    const loss = this.income - this.costs;
    return loss < 0 ? loss : 0;
  }

  public getAdditionalCosts(sellStockTransaction: StockTransaction) {
    return this.originQuantitySoldRatio * (sellStockTransaction.commission + sellStockTransaction.tax);
  }

  public getTransactionDate() {
    return null;
  }
}
