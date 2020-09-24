from apps.stocks.markets.models import Company
from apps.stocks.transactions.models import StockSplitTransaction
from apps.stocks.transactions.utils.utils import get_stock_splits

SOURCES = {'Yahoo'}


def populate_stock_splits_data(source, file_path=None):
    splits = get_stock_splits(source=source, file_path=file_path)
    stock_split_objects = []

    for (symbol, pay_date, optional, ratio_from, ratio_for) in splits:
        companies = Company.objects.filter(symbol=symbol)

        if companies.exists():

            stock_split = StockSplitTransaction(
                company=companies.first(), pay_date=pay_date, optional=optional,
                exchange_ratio_from=ratio_for, exchange_ratio_for=ratio_for)

            stock_split_objects.append(stock_split)

    StockSplitTransaction.objects.bulk_create(stock_split_objects)


def populate_all_stock_splits_data():
    for source in SOURCES:
        populate_stock_splits_data(source=source)
