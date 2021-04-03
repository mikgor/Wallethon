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
import {SellRelatedBuyStockTransaction} from '../../../../shared/models/transactions-summary/sell-related-buy-stock-transaction';
import {SellRelatedStockDividendTransaction} from '../../../../shared/models/transactions-summary/sell-related-stock-dividend-transaction';
import {SellStockTransactionSummary} from '../../../../shared/models/transactions-summary/sell-stock-transaction-summary';
import {StockSummary} from '../../../../shared/models/transactions-summary/stock-summary';
import {UserBrokerStockSummary} from '../../../../shared/models/transactions-summary/user-broker-stock-summary';
import {MoneyService} from '../../../../shared/services/money.service';
import {SellRelatedTransaction} from '../../../../shared/models/transactions-summary/sell-related-transaction';
import {CashDividendTransactionSummary} from '../../../../shared/models/transactions-summary/cash-dividend-transaction-summary';

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  constructor(
    private http: HttpClient,
    private requestsService: RequestsService,
    private moneyService: MoneyService
  ) {}

  public getTransactionType(transaction) {
    return transaction.constructor.name;
  }

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
    return this.requestsService.getRequest(`stocksplittransactions/?related=true`).pipe(
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

  public getSellRelatedBuyStockTransactionFromResponse(response) {
    return new SellRelatedBuyStockTransaction(
      this.getStockTransactionFromResponse(response.buy_stock_transaction),
      Number(response.sold_quantity),
      Number(response.origin_quantity_sold_ratio),
      response.costs,
      response.costs_currency,
      response.income,
      response.income_currency,
    );
  }

  public getSellRelatedBuyStockTransactionsFromResponse(response) {
    const sellRelatedBuyStockTransactions: SellRelatedBuyStockTransaction[] = [];
    for (const sellRelatedBuyStockTransaction of response) {
      sellRelatedBuyStockTransactions.push(
        this.getSellRelatedBuyStockTransactionFromResponse(sellRelatedBuyStockTransaction));
    }
    return sellRelatedBuyStockTransactions;
  }

  public getSellRelatedStockDividendTransactionFromResponse(response) {
    return new SellRelatedStockDividendTransaction(
      this.getStockDividendTransactionFromResponse(response.stock_dividend_transaction),
      Number(response.sold_quantity),
      Number(response.origin_quantity_sold_ratio),
      response.costs,
      response.costs_currency,
      response.income,
      response.income_currency,
    );
  }

  public getSellRelatedStockDividendTransactionsFromResponse(response) {
    const sellRelatedStockDividendTransactions: SellRelatedStockDividendTransaction[] = [];
    for (const sellRelatedStockDividendTransaction of response) {
      sellRelatedStockDividendTransactions.push(
        this.getSellRelatedStockDividendTransactionFromResponse(sellRelatedStockDividendTransaction));
    }
    return sellRelatedStockDividendTransactions;
  }

  public getSellStockTransactionSummaryFromResponse(response) {
    return new SellStockTransactionSummary(
      this.getStockTransactionFromResponse(response.sell_stock_transaction),
      this.getSellRelatedBuyStockTransactionsFromResponse(response.sell_related_buy_stock_transactions),
      this.getSellRelatedStockDividendTransactionsFromResponse(response.sell_related_stock_dividend_transactions),
      );
  }

  public getSellStockTransactionsSummariesFromResponse(response) {
    const sellStockTransactionSummaries: SellStockTransactionSummary[] = [];
    for (const sellStockTransactionSummary of response) {
      sellStockTransactionSummaries.push(
        this.getSellStockTransactionSummaryFromResponse(sellStockTransactionSummary));
    }
    return sellStockTransactionSummaries;
  }

  public getCashDividendTransactionSummaryFromResponse(response) {
    return new CashDividendTransactionSummary(
        this.getCashDividendTransactionFromResponse(response.cash_dividend_transaction),
        response.income,
        response.income_currency
    );
  }

  public getCashDividendTransactionsSummariesFromResponse(response) {
    const cashDividendTransactionSummaries: CashDividendTransactionSummary[] = [];
    for (const cashDividendTransactionSummary of response) {
      cashDividendTransactionSummaries.push(
        this.getCashDividendTransactionSummaryFromResponse(cashDividendTransactionSummary));
    }
    return cashDividendTransactionSummaries;
  }

  public getStockSummaryFromResponse(response) {
    return new StockSummary(
      this.getCompanyStockFromResponse(response.company_stock),
      this.getStockTransactionsFromResponse(response.buy_stock_transactions),
      this.getSellStockTransactionsSummariesFromResponse(response.sell_stock_transactions_summaries),
      this.getStockSplitTransactionsFromResponse(response.stock_split_transactions),
      this.getStockDividendTransactionsFromResponse(response.stock_dividend_transactions),
      this.getCashDividendTransactionsSummariesFromResponse(response.cash_dividend_transactions_summaries),
      response.cash_dividend_total,
      response.stock_dividend_total,
      response.remaining_stock_quantity,
      );
  }

  public getStockSummariesFromResponse(response) {
    const stockSummaries: StockSummary[] = [];
    for (const stockSummary of response) {
      stockSummaries.push(this.getStockSummaryFromResponse(stockSummary));
    }
    return stockSummaries;
  }

  public getUserBrokerStockSummaryFromResponse(response) {
    return new UserBrokerStockSummary(
      response.uuid,
      new Date(response.date_from),
      new Date(response.date_to),
      this.getUserBrokerFromResponse(response.user_broker),
      response.currency,
      this.getStockSummariesFromResponse(response.stock_summaries)
      );
  }

  public getTransactionsSummary(brokerId, dateFrom, dateTo) {
    const data = {
      date_from: dateFrom,
      date_to: dateTo,
      user_broker_id: brokerId,
      currency: 'PLN'
    };
    return this.requestsService.postRequest('transactionssummary/', data).pipe(
      map((response) => {
        return this.getUserBrokerStockSummaryFromResponse(response);
      })
    );
  }

  private calculateSellRelatedTransaction(sellRelatedTransactions: SellRelatedTransaction[],
                                          sellStockTransaction: StockTransaction, currency: string) {
    for (const sellRelatedTransaction of sellRelatedTransactions) {
      const income = sellStockTransaction.perStockPrice.multiply(sellRelatedTransaction.soldQuantity);
      const costs = sellRelatedTransaction.getAdditionalCosts(sellStockTransaction);
      if (!income.currencyEquals(currency) || !costs.currencyEquals(currency)) {
        this.moneyService.getExchangedValue(income, sellStockTransaction.date, currency).subscribe(incomeExchanged =>
            this.moneyService.getExchangedValue(costs, sellRelatedTransaction.getTransactionDate(), currency).subscribe(costsExchanged =>
            sellRelatedTransaction.setCostsAndIncome(costsExchanged, incomeExchanged))
        );
      } else {
        sellRelatedTransaction.setCostsAndIncome(costs, income);
      }
    }
  }

  public calculateProfitFromUserBrokerStockSummary(userBrokerStockSummary: UserBrokerStockSummary, currency: string) {
    for (const stockSummary of userBrokerStockSummary.stockSummaries) {
      for (const sellStockTransactionsSummary of stockSummary.sellStockTransactionsSummaries) {
        this.calculateSellRelatedTransaction(sellStockTransactionsSummary.sellRelatedBuyStockTransactions,
          sellStockTransactionsSummary.sellStockTransaction, currency);
        this.calculateSellRelatedTransaction(sellStockTransactionsSummary.sellRelatedStockDividendTransactions,
          sellStockTransactionsSummary.sellStockTransaction, currency);
      }
      for (const cashDividendTransactionsSummary of stockSummary.cashDividendTransactionsSummaries) {
        const cashDividendTransaction = cashDividendTransactionsSummary.cashDividendTransaction;
        if (!cashDividendTransaction.totalValue.currencyEquals(currency)) {
          this.moneyService.getExchangedValue(cashDividendTransaction.totalValue, cashDividendTransaction.date,
            currency).subscribe(incomeExchanged =>
            cashDividendTransactionsSummary.setIncome(incomeExchanged)
          );
        }
      }
    }
  }
}
