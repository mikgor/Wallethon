from datetime import date

from apps.stocks.utils import currency_exchange


def get_currency_exchange_rate(currency_code_from: str, currency_code_to: str, exchange_date: date):

    if currency_code_to == 'PLN':
        return currency_exchange.get_nbp_mid_exchange_rate(
            currency_code=currency_code_from, exchange_date=exchange_date)

    return None
