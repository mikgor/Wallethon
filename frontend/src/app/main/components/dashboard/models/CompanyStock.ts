import {Company} from './Company';

export class CompanyStock {
  id: string;
  company: Company;
  symbol: string;
  details: string;

  constructor(id: string, company: Company, symbol: string, details: string) {
    this.id = id;
    this.company = company;
    this.symbol = symbol;
    this.details = details;
  }
}
