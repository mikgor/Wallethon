from apps.stocks.utils import nasdaq


def get_market_stock_companies(market_symbol):

    if market_symbol == 'NASDAQ':
        return nasdaq.get_stock_companies_symbols_tuples()

    return None
