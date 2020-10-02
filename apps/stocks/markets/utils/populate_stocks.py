from apps.stocks.markets.models import Market, Company, MarketCompanyStock, CompanyStock
from apps.stocks.markets.utils import nasdaq, gpw, nyse_bats_iexg_stocks

MARKETS = {'NASDAQ', 'GPW', *nyse_bats_iexg_stocks.MARKETS.keys()}


def get_market_stock_companies(market_name, from_file=False, file_path=None):

    if market_name == 'NASDAQ':
        return nasdaq.get_stock_companies_symbols_tuples(from_file=from_file, file_path=file_path)

    if market_name == 'GPW':
        return gpw.get_stock_companies_symbols_tuples(file_path=file_path)

    if market_name in nyse_bats_iexg_stocks.MARKETS.keys():
        return nyse_bats_iexg_stocks.get_stock_companies_symbols_tuples(market_name=market_name, file_path=file_path)

    return None


def populate_stocks_data(market_name=None, from_file=True, file_path=None):
    companies = get_market_stock_companies(market_name=market_name, from_file=from_file, file_path=file_path)
    market = Market.objects.create(name=market_name)
    company_objects = []
    company_stock_objects = []
    market_company_stock_objects = []

    for (symbol, company_name, company_details) in companies:
        company_matches = [c for c in company_objects if c.name == company_name]
        company = company_matches[0] if len(company_matches) > 0 else Company(name=company_name)
        company_stock = CompanyStock(company=company, symbol=symbol, details=company_details)
        market_company_stock = MarketCompanyStock(market=market, company_stock=company_stock)

        if len(company_matches) == 0:
            company_objects.append(company)
        company_stock_objects.append(company_stock)
        market_company_stock_objects.append(market_company_stock)

    Company.objects.bulk_create(company_objects)
    CompanyStock.objects.bulk_create(company_stock_objects)
    MarketCompanyStock.objects.bulk_create(market_company_stock_objects)


def populate_all_stocks_data():
    for market in MARKETS:
        print(f'Populating {market}...')
        populate_stocks_data(market_name=market)


def populate_market_stocks_data(market_name=None, from_file=True, file_path=None):
    populate_stocks_data(market_name=market_name, from_file=from_file, file_path=file_path)
