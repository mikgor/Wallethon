import {CompanyStock} from './CompanyStock';
import {UserBroker} from './UserBroker';
import {Money} from '../../../../shared/models/money';


export class CashDividendTransaction {
  id: string;
  companyStock: CompanyStock;
  date: Date;
  dividend: Money;
  tax: Money;
  commission: Money;
  totalValue: Money;
  broker: UserBroker;

  constructor(id: string, companyStock: CompanyStock, date: Date, dividend: number,
              dividendCurrency: string, tax: number, taxCurrency: string, commission: number,
              commissionCurrency: string, totalValue: number, totalValueCurrency: string, broker: UserBroker) {
    this.id = id;
    this.companyStock = companyStock;
    this.date = date;
    this.dividend = new Money(dividend, dividendCurrency);
    this.tax = new Money(tax, taxCurrency);
    this.commission = new Money(commission, commissionCurrency);
    this.totalValue = new Money(totalValue, totalValueCurrency);
    this.broker = broker;
  }

  public getTotalValueText() {
    return 'Total value (dividend - [tax + commissions]) =\n'
      + ` (${this.dividend.toRepresentation()}`
      + ` - [${this.tax.toRepresentation()}`
      + ` + ${this.commission.toRepresentation()}])`;
  }
}
