from apps.stocks.transactions.utils import yahoo, revolut


def get_stock_splits(source, file_path=None):
    if source == 'Yahoo':
        return yahoo.get_stock_splits_tuples(file_path=file_path)

    return None


def get_transactions_from_files(source, files_paths):
    if source == 'Revolut':
        return revolut.get_transactions_tuples_from_files(files_paths=files_paths)

    return None
