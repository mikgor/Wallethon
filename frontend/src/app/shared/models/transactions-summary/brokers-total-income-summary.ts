import {BrokerIncomeSummary} from './broker-income-summary';

export class BrokersTotalIncomeSummary {
  brokerIncomeSummaries: BrokerIncomeSummary[];
  taxRate: number;

  public constructor(taxRate: number, brokerIncomeSummaries: BrokerIncomeSummary[]) {
    this.taxRate = taxRate;
    this.brokerIncomeSummaries = brokerIncomeSummaries;
  }

  public income() {
    let income = 0.00;
    for (const brokerIncomeSummary of this.brokerIncomeSummaries) {
      income += brokerIncomeSummary.income();
    }
    return income;
  }

  public cashDividendIncome() {
    let cashDividendIncome = 0.00;
    for (const brokerIncomeSummary of this.brokerIncomeSummaries) {
      cashDividendIncome += brokerIncomeSummary.cashDividendIncome();
    }
    return cashDividendIncome;
  }

  public incomeTax() {
    return this.income() * this.taxRate;
  }

  public cashDividendIncomeTax() {
    return this.cashDividendIncome() * this.taxRate;
  }
}
