import {CompanyStock} from './CompanyStock';
import {UserBroker} from './UserBroker';

export class StockDividendTransaction {
  id: string;
  companyStock: CompanyStock;
  stockQuantity: number;
  date: Date;
  broker: UserBroker;

  constructor(id: string, companyStock: CompanyStock, stockQuantity: number, date: Date,
              broker: UserBroker) {
    this.id = id;
    this.companyStock = companyStock;
    this.stockQuantity = Number(stockQuantity);
    this.date = date;
    this.broker = broker;
  }
}
