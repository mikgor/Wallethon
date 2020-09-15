from apps.stocks.utils import nasdaq


def get_market_stock_companies(market_name, from_file=False, file_path=None):

    if market_name == 'NASDAQ':
        return nasdaq.get_stock_companies_symbols_tuples(from_file=from_file, file_path=file_path)

    return None
