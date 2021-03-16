from apps.stocks.transactions.utils import yahoo, revolut

from apps.stocks.transactions.models import StockSplitTransaction, StockTransaction, StockDividendTransaction


def sorted_transactions(transactions, reverse=False):
    return sorted(transactions, key=lambda x: x.timestamp(), reverse=reverse)


def sum_user_stocks_quantities(transaction_type, user, stocks_quantities=None):
    transactions = transaction_type.objects.filter(user=user)

    if stocks_quantities is None:
        # {'stock_id': total_stock_quantity}
        stocks_quantities = {}

    for transaction in transactions:
        stock_id = transaction.company_stock.id
        stock_quantity = transaction.stock_quantity

        if hasattr(transaction, 'type') and transaction.type == 'SELL':
            stock_quantity *= -1

        if stock_id in stocks_quantities:
            stocks_quantities[stock_id] += stock_quantity
        else:
            stocks_quantities[stock_id] = stock_quantity

    return stocks_quantities


def get_user_related_stock_split_transactions(user):
    user_stock_transactions_quantities = sum_user_stocks_quantities(StockTransaction, user)
    stocks_quantities = sum_user_stocks_quantities(StockDividendTransaction, user, user_stock_transactions_quantities)
    filtered_stocks_quantities = {stock: amount for (stock, amount) in stocks_quantities.items()}

    return StockSplitTransaction.objects.filter(company_stock__id__in=filtered_stocks_quantities.keys())


def get_stock_splits(source, file_path=None):
    if source == 'Yahoo':
        return yahoo.get_stock_splits_tuples(file_path=file_path)

    return None


def get_transactions_from_files(source, files_paths):
    if source == 'Revolut':
        return revolut.get_transactions_tuples_from_files(files_paths=files_paths)

    return None
