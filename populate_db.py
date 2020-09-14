"""
Adds random data to database
Run this script after migrations
"""
import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
application = get_wsgi_application()

from apps.stocks.transactions.models import StockTransaction
from main.tests.utils.base_case import BaseTestCase

v = BaseTestCase()
superuser, password = v.create_superuser()
print('email: %s password: %s' % (superuser.email, password))
market = v.create_market()
company = v.create_company()
market_company = v.create_market_company(market=market, company=company)
user_stock_transaction = v.create_user_stock_transaction(user=superuser)
stock_transaction = StockTransaction.objects.get(pk=user_stock_transaction.transaction.pk)
print("{s.id} {s.type} {s.company} {s.stock_quantity} {s.per_stock_price} "
      "{s.commission_and_tax} {s.total_value} {s.date}".format(s=stock_transaction))
