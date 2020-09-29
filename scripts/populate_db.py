"""
Adds random data to database
Run this script after migrations
"""
import os
from django.core.wsgi import get_wsgi_application

from apps.stocks.transactions.models import UserBroker
from apps.stocks.transactions.utils.populate_stock_splits import populate_all_stock_splits_data

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
application = get_wsgi_application()

from main.tests.utils.base_case import BaseTestCase
from apps.stocks.markets.models import CompanyStock
from apps.stocks.markets.utils.populate_stocks import populate_market_stocks_data


def populate_db():
    v = BaseTestCase()
    superuser, password = v.create_superuser()
    print('email: %s password: %s' % (superuser.email, password))

    populate_market_stocks_data(
        market_name='NASDAQ', from_file=True,
        file_path='apps/stocks/markets/utils/data/nasdaq_stocks.txt'
    )

    populate_all_stock_splits_data()

    broker = v.create_user_broker(user=superuser)
    broker2 = v.create_user_broker(user=superuser)

    for i in range(15):
        random_company_stock = CompanyStock.objects.order_by('?')[0]
        random_broker = UserBroker.objects.order_by('?')[0]
        v.create_stock_transaction(user=superuser, company_stock=random_company_stock, broker=random_broker)

    for i in range(10):
        random_company_stock = CompanyStock.objects.order_by('?')[0]
        random_broker = UserBroker.objects.order_by('?')[0]
        v.create_cash_dividend_transaction(user=superuser, company_stock=random_company_stock, broker=random_broker)
        v.create_stock_dividend_transaction(user=superuser, company_stock=random_company_stock, broker=random_broker)
        v.create_stock_split_transaction(company_stock=random_company_stock)
        v.create_stock_transaction(user=superuser, company_stock=random_company_stock, broker=random_broker)
