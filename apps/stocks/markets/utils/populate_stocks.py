from apps.stocks.markets.models import Market, Company, MarketCompany
from apps.stocks.markets.utils.utils import get_market_stock_companies

MARKETS = {'NASDAQ'}


def populate_stocks_data(market_name=None, from_file=True, file_path=None):
    companies = get_market_stock_companies(market_name=market_name, from_file=from_file, file_path=file_path)
    market = Market.objects.create(name=market_name)
    company_objects = []
    market_company_objects = []

    for (symbol, company_name) in companies:
        company = Company(name=company_name, symbol=symbol)
        market_company = MarketCompany(market=market, company=company)

        company_objects.append(company)
        market_company_objects.append(market_company)

    Company.objects.bulk_create(company_objects)
    MarketCompany.objects.bulk_create(market_company_objects)


def populate_all_stocks_data():
    for market in MARKETS:
        populate_stocks_data(market_name=market)


def populate_market_stocks_data(market_name=None, from_file=True, file_path=None):
    populate_stocks_data(market_name=market_name, from_file=from_file, file_path=file_path)
