import requests
from datetime import date


def get_nbp_mid_exchange_rate(currency_code: str, exchange_date: date):
    endpoint = 'https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{date}'\
        .format(currency_code=currency_code, date=exchange_date.strftime("%Y-%m-%d"))
    response = requests.get(endpoint)

    # 404 when invalid date
    if response.status_code == 400 or response.status_code == 404:
        return None

    return response.json()['rates'][0]['mid']

