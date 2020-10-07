import {CompanyStock} from './CompanyStock';
import {UserBroker} from './UserBroker';
import {MoneyService} from '../../../../shared/services/money.service';


export class CashDividendTransaction {
  id: string;
  companyStock: CompanyStock;
  date: Date;
  dividend: number;
  dividendCurrency: string;
  tax: number;
  taxCurrency: string;
  commission: number;
  commissionCurrency: string;
  totalValue: number;
  totalValueCurrency: string;
  broker: UserBroker;

  constructor(id: string, companyStock: CompanyStock, date: Date, dividend: number,
              dividendCurrency: string, tax: number, taxCurrency: string, commission: number,
              commissionCurrency: string, totalValue: number, totalValueCurrency: string, broker: UserBroker) {
    this.id = id;
    this.companyStock = companyStock;
    this.date = date;
    this.dividend = Number(dividend);
    this.dividendCurrency = dividendCurrency;
    this.tax = Number(tax);
    this.taxCurrency = taxCurrency;
    this.commission = Number(commission);
    this.commissionCurrency = commissionCurrency;
    this.totalValue = Number(totalValue);
    this.totalValueCurrency = totalValueCurrency;
    this.broker = broker;
  }

  public getTotalValueText() {
    return 'Total value (dividend - [tax + commissions]) =\n'
      + ` (${MoneyService.formatMoney(this.dividend, this.dividendCurrency)}`
      + ` - [${MoneyService.formatMoney(this.tax, this.taxCurrency)}`
      + ` + ${MoneyService.formatMoney(this.commission, this.commissionCurrency)}])`;
  }
}
