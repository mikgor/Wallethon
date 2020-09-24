from apps.stocks.transactions.utils import yahoo


def get_stock_splits(source, file_path=None):

    if source == 'Yahoo':
        return yahoo.get_stock_splits_tuples(file_path=file_path)

    return None
