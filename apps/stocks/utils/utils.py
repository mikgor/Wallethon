from apps.stocks.utils import nasdaq


def get_market_stock_companies(market_symbol, file_path=None):

    if market_symbol == 'NASDAQ':
        return nasdaq.get_stock_companies_symbols_tuples(file_path=file_path)

    return None
