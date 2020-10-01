import {CompanyStock} from './CompanyStock';
import {UserBroker} from './UserBroker';
import {MoneyService} from "../../../../shared/services/money.service";

export class StockTransaction {
  id: string;
  type: string;
  companyStock: CompanyStock;
  date: Date;
  perStockPrice: number;
  perStockPriceCurrency: string;
  stockQuantity: number;
  tax: number;
  taxCurrency: string;
  commission: number;
  commissionCurrency: string;
  totalValue: number;
  totalValueCurrency: string;
  broker: UserBroker;

  constructor(id: string, type: string, companyStock: CompanyStock, date: Date, perStockPrice: number,
              perStockPriceCurrency: string, stockQuantity: number, tax: number, taxCurrency: string,
              commission: number, commissionCurrency: string, totalValue: number, totalValueCurrency: string,
              broker: UserBroker) {
    this.id = id;
    this.type = type;
    this.companyStock = companyStock;
    this.date = date;
    this.perStockPrice = perStockPrice;
    this.perStockPriceCurrency = perStockPriceCurrency;
    this.stockQuantity = stockQuantity;
    this.tax = tax;
    this.taxCurrency = taxCurrency;
    this.commission = commission;
    this.commissionCurrency = commissionCurrency;
    this.totalValue = totalValue;
    this.totalValueCurrency = totalValueCurrency;
    this.broker = broker;
  }

  public getTotalValueText() {
    return 'Total value (price per stock * stock quantity + tax + commissions) =\n'
      + ` (${MoneyService.formatMoney(this.perStockPrice, this.perStockPriceCurrency)}`
      + ` * ${this.stockQuantity} +`
      + ` ${MoneyService.formatMoney(this.tax, this.taxCurrency)}`
      + ` + ${MoneyService.formatMoney(this.commission, this.commissionCurrency)})`;
  }
}
