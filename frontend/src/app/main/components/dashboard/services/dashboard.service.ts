import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';
import {StockTransaction} from '../models/StockTransaction';
import {CompanyStock} from '../models/CompanyStock';
import {Company} from '../models/Company';
import {StockSplitTransaction} from '../models/StockSplitTransaction';
import {RequestsService} from '../../../../shared/services/requests.service';
import {StockDividendTransaction} from '../models/StockDividendTransaction';
import {CashDividendTransaction} from '../models/CashDividendTransaction';
import {UserBroker} from '../models/UserBroker';

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  constructor(
    private http: HttpClient,
    private requestsService: RequestsService,
  ) {}

  public getCompanies() {
    return this.requestsService.getRequest('companies/').pipe(
      map((response) => {
        return this.getCompaniesFromResponse(response);
      })
    );
  }

  public getCompanyById(id: string) {
    return this.requestsService.getRequest(`companies/${id}/`).pipe(
      map((response) => {
        return this.getCompanyFromResponse(response);
      })
    );
  }

  public getUserBrokers() {
    return this.requestsService.getRequest(`userbrokers/`).pipe(
      map((response) => {
        return this.getUserBrokersFromResponse(response);
      })
    );
  }

  public getUserBrokerById(id: string) {
    return this.requestsService.getRequest(`userbrokers/${id}/`).pipe(
      map((response) => {
        return this.getUserBrokerFromResponse(response);
      })
    );
  }

  public getCompanyStocksWithFilters(filters: string = '') {
    return this.requestsService.getRequest(`companystocks/?${filters}`).pipe(
      map((response) => {
        return this.getCompanyStocksFromResponse(response);
      })
    );
  }

  public getCompanyStocks() {
    return this.getCompanyStocksWithFilters();
  }

  public getCompanyStockById(id: string) {
    return this.requestsService.getRequest(`companystocks/${id}/`).pipe(
      map((response) => {
        return this.getCompanyStockFromResponse(response);
      })
    );
  }

  public getStockTransactions() {
    return this.requestsService.getRequest('stocktransactions/').pipe(
      map((response) => {
        return this.getStockTransactionsFromResponse(response);
      })
    );
  }

  public getStockTransactionById(id: string) {
    return this.requestsService.getRequest(`stocktransactions/${id}/`).pipe(
      map((response) => {
        return this.getStockTransactionFromResponse(response);
      })
    );
  }

  public getStockSplitTransactionById(id: string) {
    return this.requestsService.getRequest(`stocksplittransactions/${id}/`).pipe(
      map((response) => {
        return this.getStockSplitTransactionFromResponse(response);
      })
    );
  }

  public getStockSplitTransactions() {
    return this.requestsService.getRequest(`stocksplittransactions/?filtered=true`).pipe(
      map((response) => {
        return this.getStockSplitTransactionsFromResponse(response);
      })
    );
  }

  public getCashDividendTransactionById(id: string) {
    return this.requestsService.getRequest(`cashdividendtransactions/${id}/`).pipe(
      map((response) => {
        return this.getCashDividendTransactionFromResponse(response);
      })
    );
  }

  public getCashDividendTransactions() {
    return this.requestsService.getRequest(`cashdividendtransactions/`).pipe(
      map((response) => {
        return this.getCashDividendTransactionsFromResponse(response);
      })
    );
  }

  public getStockDividendTransactionById(id: string) {
    return this.requestsService.getRequest(`stockdividendtransactions/${id}/`).pipe(
      map((response) => {
        return this.getStockDividendTransactionFromResponse(response);
      })
    );
  }

  public getStockDividendTransactions() {
    return this.requestsService.getRequest(`stockdividendtransactions/`).pipe(
      map((response) => {
        return this.getStockDividendTransactionsFromResponse(response);
      })
    );
  }

  public getCompanyFromResponse(response) {
    return new Company(
      response.uuid,
      response.name
    );
  }

  public getUserBrokersFromResponse(response) {
    const userBrokers: UserBroker[] = [];
    for (const userBroker of response) {
      userBrokers.push(this.getUserBrokerFromResponse(userBroker));
    }
    return userBrokers;
  }

  public getUserBrokerFromResponse(response) {
    return new UserBroker(
      response.uuid,
      response.broker_name
    );
  }

  public getCompaniesFromResponse(response) {
    const companies: Company[] = [];
    for (const company of response) {
      companies.push(this.getCompanyFromResponse(company));
    }
    return companies;
  }

  public getCompanyStockFromResponse(response) {
    return new CompanyStock(
      response.uuid,
      this.getCompanyFromResponse(response.company),
      response.symbol,
      response.details
    );
  }

  public getCompanyStocksFromResponse(response) {
    const companyStocks: CompanyStock[] = [];
    for (const companyStock of response) {
      companyStocks.push(this.getCompanyStockFromResponse(companyStock));
    }
    return companyStocks;
  }

  public getStockTransactionFromResponse(response) {
    return new StockTransaction(
      response.uuid,
      response.type,
      this.getCompanyStockFromResponse(response.company_stock),
      new Date(response.date),
      response.per_stock_price,
      response.per_stock_price_currency,
      response.stock_quantity,
      response.tax,
      response.tax_currency,
      response.commission,
      response.commission_currency,
      response.total_value,
      response.total_value_currency,
      this.getUserBrokerFromResponse(response.broker),
    );
  }

  public getStockTransactionsFromResponse(response) {
    const stockTransactions: StockTransaction[] = [];
    for (const stockTransaction of response) {
      stockTransactions.push(this.getStockTransactionFromResponse(stockTransaction));
    }

    return stockTransactions;
  }

  public getStockSplitTransactionFromResponse(response) {
    const date = new Date(response.pay_date);
    date.setHours(0, 0, 0, 0);

    return new StockSplitTransaction(
      response.uuid,
      this.getCompanyStockFromResponse(response.company_stock),
      response.exchange_ratio_from,
      response.exchange_ratio_for,
      response.optional,
      date,
    );
  }

  public getStockSplitTransactionsFromResponse(response) {
    const stockSplitTransactions: StockSplitTransaction[] = [];
    for (const stockSplitTransaction of response) {
      stockSplitTransactions.push(this.getStockSplitTransactionFromResponse(stockSplitTransaction));
    }
    return stockSplitTransactions;
  }

  public getCashDividendTransactionFromResponse(response) {
    return new CashDividendTransaction(
      response.uuid,
      this.getCompanyStockFromResponse(response.company_stock),
      new Date(response.date),
      response.dividend,
      response.dividend_currency,
      response.tax,
      response.tax_currency,
      response.commission,
      response.commission_currency,
      response.total_value,
      response.total_value_currency,
      this.getUserBrokerFromResponse(response.broker),
    );
  }

  public getCashDividendTransactionsFromResponse(response) {
    const cashDividendTransactions: CashDividendTransaction[] = [];
    for (const cashDividendTransaction of response) {
      cashDividendTransactions.push(this.getCashDividendTransactionFromResponse(cashDividendTransaction));
    }
    return cashDividendTransactions;
  }

  public getStockDividendTransactionFromResponse(response) {
    return new StockDividendTransaction(
      response.uuid,
      this.getCompanyStockFromResponse(response.company_stock),
      response.stock_quantity,
      new Date(response.date),
      this.getUserBrokerFromResponse(response.broker),
    );
  }

  public getStockDividendTransactionsFromResponse(response) {
    const stockDividendTransactions: StockDividendTransaction[] = [];
    for (const stockDividendTransaction of response) {
      stockDividendTransactions.push(this.getStockDividendTransactionFromResponse(stockDividendTransaction));
    }
    return stockDividendTransactions;
  }
}
