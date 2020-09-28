import {CompanyStock} from './CompanyStock';

export class StockSplitTransaction {
  id: string;
  companyStock: CompanyStock;
  exchangeRatioFrom: number;
  exchangeRatioFor: number;
  optional: boolean;
  date: Date;

  constructor(id: string, companyStock: CompanyStock, exchangeRatioFrom: number,
              exchangeRatioFor: number, optional: boolean, payDate: Date) {
    this.id = id;
    this.companyStock = companyStock;
    this.exchangeRatioFrom = exchangeRatioFrom;
    this.exchangeRatioFor = exchangeRatioFor;
    this.optional = optional;
    this.date = payDate;
  }
}
