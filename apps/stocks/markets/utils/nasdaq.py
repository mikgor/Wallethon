from apps.stocks.markets.utils.utils import download_stock_companies_data_ftp, \
    read_nasdaq_stock_companies_symbols_tuples_from_file

FTP_SERVER = 'ftp.nasdaqtrader.com'
FTP_FILE_PATH = 'SymbolDirectory/nasdaqlisted.txt'
DESTINATION_FILE = 'apps/stocks/markets/utils/data/nasdaq_stocks.txt'


def get_stock_companies_symbols_tuples(from_file=False, file_path=None):
    if file_path is None:
        file_path = DESTINATION_FILE

    if not from_file:
        download_stock_companies_data_ftp(FTP_SERVER, FTP_FILE_PATH, from_file)

    return read_nasdaq_stock_companies_symbols_tuples_from_file(file_path)
