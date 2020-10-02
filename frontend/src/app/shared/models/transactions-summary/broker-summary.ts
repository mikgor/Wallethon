import {UserBroker} from '../../../main/components/dashboard/models/UserBroker';
import {CompanyStock} from '../../../main/components/dashboard/models/CompanyStock';
import {StockSplitTransaction} from '../../../main/components/dashboard/models/StockSplitTransaction';
import {StockSummary} from './stock-summary';

export class BrokerSummary {
  broker: UserBroker;
  stockSummaries: StockSummary[];

  constructor(broker: UserBroker) {
    this.broker = broker;
    this.stockSummaries = [];
  }

  public getStockSummary(companyStock: CompanyStock) {
    let stockSummary: StockSummary = this.stockSummaries.filter(x => x.companyStock.id === companyStock.id)[0];
    if (stockSummary === undefined) {
      const newStockSummary = new StockSummary(companyStock);
      this.stockSummaries.push(newStockSummary);
      stockSummary = newStockSummary;
    }
    return stockSummary;
  }

  private getStockSummaryIndex(companyStock: CompanyStock) {
    return this.stockSummaries.indexOf(this.getStockSummary(companyStock));
  }

  private updateStockSummary(stockSummary: StockSummary) {
    this.stockSummaries[this.getStockSummaryIndex(stockSummary.companyStock)] = stockSummary;
  }

  public calculateStockSplitTransaction(stockSplitTransaction: StockSplitTransaction) {
    const stockSummary: StockSummary = this.getStockSummary(stockSplitTransaction.companyStock);
    stockSummary.calculateStockSplitTransaction(stockSplitTransaction);
    this.updateStockSummary(stockSummary);
  }
}
