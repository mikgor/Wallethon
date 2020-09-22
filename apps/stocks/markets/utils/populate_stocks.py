from apps.stocks.markets.models import Market, Company, MarketCompany
from apps.stocks.markets.utils.utils import get_market_stock_companies

MARKETS = {'NASDAQ'}


def populate_stocks_data(market_name=None, from_file=True, file_path=None):
    companies = get_market_stock_companies(market_name=market_name, from_file=from_file, file_path=file_path)

    market = Market.objects.create(name=market_name)

    for (symbol, company_name) in companies:
        company = Company.objects.create(name=company_name, symbol=symbol)
        MarketCompany.objects.create(market=market, company=company)


def populate_all_stocks_data():
    for market in MARKETS:
        populate_stocks_data(market_name=market)


def populate_market_stocks_data(market_name=None, from_file=True, file_path=None):
    populate_stocks_data(market_name=market_name, from_file=from_file, file_path=file_path)
