import {Injectable} from '@angular/core';
import {RequestsService} from './requests.service';
import {map} from "rxjs/operators";
import {StockTransaction} from "../../main/components/dashboard/models/StockTransaction";
import {AuthService} from "../../registration/services/auth.service";

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
      per_stock_price: stockTransaction.perStockPrice,
      per_stock_price_currency: stockTransaction.perStockPriceCurrency,
      stock_quantity: stockTransaction.stockQuantity,
      tax: stockTransaction.tax,
      tax_currency: stockTransaction.taxCurrency,
      commission: stockTransaction.commission,
      commission_currency: stockTransaction.commissionCurrency,
      broker_id: stockTransaction.broker.id,
      user: this.authService.getCurrentUser().id
    };
    return this.requestsService.postRequest(`stocktransactions/`, data);
  }
}
