from datetime import date

from apps.stocks.utils import nasdaq, currency_exchange


def get_market_stock_companies(market_name, from_file=False, file_path=None):

    if market_name == 'NASDAQ':
        return nasdaq.get_stock_companies_symbols_tuples(from_file=from_file, file_path=file_path)

    return None


def get_currency_exchange_rate(currency_code_from: str, currency_code_to: str, exchange_date: date):

    if currency_code_from == 'PLN':
        return currency_exchange.get_nbp_mid_exchange_rate(
            currency_code=currency_code_to, exchange_date=exchange_date)

    return None
