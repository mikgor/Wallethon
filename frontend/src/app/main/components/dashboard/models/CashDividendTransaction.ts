import {CompanyStock} from './CompanyStock';

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
  brokerName: string;

  constructor(id: string, companyStock: CompanyStock, date: Date, dividend: number,
              dividendCurrency: string, tax: number, taxCurrency: string, commission: number,
              commissionCurrency: string, totalValue: number, totalValueCurrency: string, brokerName: string) {
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
    this.brokerName = brokerName;
  }
}
