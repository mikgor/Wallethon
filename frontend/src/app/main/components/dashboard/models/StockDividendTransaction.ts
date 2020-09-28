import {CompanyStock} from './CompanyStock';

export class StockDividendTransaction {
  id: string;
  companyStock: CompanyStock;
  stockQuantity: number;
  date: Date;
  brokerName: string;

  constructor(id: string, companyStock: CompanyStock, stockQuantity: number, date: Date,
              brokerName: string) {
    this.id = id;
    this.companyStock = companyStock;
    this.stockQuantity = stockQuantity;
    this.date = date;
    this.brokerName = brokerName;
  }
}
