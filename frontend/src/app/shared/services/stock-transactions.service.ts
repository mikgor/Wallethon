import {Injectable} from '@angular/core';
import {RequestsService} from './requests.service';
import {StockTransaction} from '../../main/components/dashboard/models/StockTransaction';
import {AuthService} from '../../registration/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class StockTransactionsService {
  constructor(
    private requestsService: RequestsService,
    private authService: AuthService,
  ) { }

  public getStockTransactionTypes() {
    return [
      {name: 'Buy', value: 'BUY'},
      {name: 'Sell', value: 'SELL'},
    ];
  }

  public postStockTransaction(stockTransaction: StockTransaction) {
    const data = {
      type: stockTransaction.type,
      company_stock_id: stockTransaction.companyStock.id,
      date: stockTransaction.date,
      per_stock_price: stockTransaction.perStockPrice.amount,
      per_stock_price_currency: stockTransaction.perStockPrice.currency,
      stock_quantity: stockTransaction.stockQuantity,
      tax: stockTransaction.tax.amount,
      tax_currency: stockTransaction.tax.currency,
      commission: stockTransaction.commission.amount,
      commission_currency: stockTransaction.commission.currency,
      broker_id: stockTransaction.broker.id,
      user: this.authService.getCurrentUser().id
    };
    return this.requestsService.postRequest(`stocktransactions/`, data);
  }
}
