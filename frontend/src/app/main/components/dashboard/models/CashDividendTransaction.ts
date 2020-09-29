import {CompanyStock} from './CompanyStock';
import {UserBroker} from './UserBroker';


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
    this.dividend = dividend;
    this.dividendCurrency = dividendCurrency;
    this.tax = tax;
    this.taxCurrency = taxCurrency;
    this.commission = commission;
    this.commissionCurrency = commissionCurrency;
    this.totalValue = totalValue;
    this.totalValueCurrency = totalValueCurrency;
    this.broker = broker;
  }
}
