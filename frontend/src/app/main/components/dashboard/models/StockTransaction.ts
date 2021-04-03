import {CompanyStock} from './CompanyStock';
import {UserBroker} from './UserBroker';
import {Money} from '../../../../shared/models/money';

export class StockTransaction {
  id: string;
  type: string;
  companyStock: CompanyStock;
  date: Date;
  perStockPrice: Money;
  stockQuantity: number;
  tax: Money;
  commission: Money;
  totalValue: Money;
  broker: UserBroker;

  constructor(id: string, type: string, companyStock: CompanyStock, date: Date, perStockPrice: number,
              perStockPriceCurrency: string, stockQuantity: number, tax: number, taxCurrency: string,
              commission: number, commissionCurrency: string, totalValue: number, totalValueCurrency: string,
              broker: UserBroker) {
    this.id = id;
    this.type = type;
    this.companyStock = companyStock;
    this.date = date;
    this.perStockPrice =  new Money(perStockPrice, perStockPriceCurrency);
    this.stockQuantity = Number(stockQuantity);
    this.tax = new Money(tax, taxCurrency);
    this.commission = new Money(commission, commissionCurrency);
    this.totalValue = new Money(totalValue, totalValueCurrency);
    this.broker = broker;
  }

  public getTotalValueText() {
    return 'Total value (price per stock * stock quantity + tax + commissions) =\n'
      + ` (${this.perStockPrice.toRepresentation()}`
      + ` * ${this.stockQuantity} +`
      + ` ${this.tax.toRepresentation()}`
      + ` + ${this.commission.toRepresentation()})`;
  }
}
