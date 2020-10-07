import {StockIncomeSummary} from './stock-income-summary';
import {UserBroker} from '../../../main/components/dashboard/models/UserBroker';
import {CashDividendIncome} from './cash-dividend-income';

export class BrokerIncomeSummary {
  broker: UserBroker;
  cashDividendIncomeTransactions: CashDividendIncome[];
  stockIncomeSummaries: StockIncomeSummary[];

  public constructor(broker: UserBroker, cashDividendIncomeTransactions: CashDividendIncome[],
                     stockIncomeSummaries: StockIncomeSummary[]) {
    this.broker = broker;
    this.cashDividendIncomeTransactions = cashDividendIncomeTransactions;
    this.stockIncomeSummaries = stockIncomeSummaries;
  }

  public income() {
    let income = 0.00;
    for (const stockIncomeSummary of this.stockIncomeSummaries) {
      income += stockIncomeSummary.income();
    }
    return income;
  }

  public cashDividendIncome() {
    let cashDividendIncome = 0.00;
    for (const cashDividendIncomeTransaction of this.cashDividendIncomeTransactions) {
        cashDividendIncome += cashDividendIncomeTransaction.cashDividendIncome();
      }
    return cashDividendIncome;
  }
}
