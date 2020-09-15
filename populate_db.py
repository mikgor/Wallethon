"""
Adds random data to database
Run this script after migrations
"""
import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
application = get_wsgi_application()

from main.tests.utils.base_case import BaseTestCase
from apps.stocks.markets.models import Company

v = BaseTestCase()
superuser, password = v.create_superuser()
print('email: %s password: %s' % (superuser.email, password))
market = v.create_market()

for i in range(5):
    market_company = v.create_market_company(market=market)

for i in range(15):
    random_company = Company.objects.order_by('?')[0]
    stock_transaction = v.create_stock_transaction(company=random_company)
    user_stock_transaction = v.create_user_stock_transaction(user=superuser, stock_transaction=stock_transaction)
    print("{s.id} {s.type} {s.company} {s.stock_quantity} {s.per_stock_price} "
          "{s.commission} {s.tax} {s.total_value} {s.date}".format(s=stock_transaction))
