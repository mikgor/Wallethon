from apps.stocks.markets.utils.utils import download_stock_companies_data_ftp, \
    read_nasdaq_stock_companies_symbols_tuples_from_file

FTP_SERVER = 'ftp.nasdaqtrader.com'
FTP_FILE_PATH = 'SymbolDirectory/otherlisted.txt'
DESTINATION_FILE = 'apps/stocks/markets/utils/data/nyse_bats_iexg_stocks.txt'
MARKETS = {
    'NYSE_MKT': {'data_symbol': 'A', 'destination_file': 'apps/stocks/markets/utils/data/nyse_mkt_stocks.txt'},
    'NYSE': {'data_symbol': 'N', 'destination_file': 'apps/stocks/markets/utils/data/nyse_stocks.txt'},
    'NYSE_ARCA': {'data_symbol': 'P', 'destination_file': 'apps/stocks/markets/utils/data/nyse_arca_stocks.txt'},
    'BATS': {'data_symbol': 'Z', 'destination_file': 'apps/stocks/markets/utils/data/bats_stocks.txt'},
    'IEXG': {'data_symbol': 'V', 'destination_file': 'apps/stocks/markets/utils/data/iexg_stocks.txt'},
}


def download_markets_data():
    lines_starts_to_ignore = ('ACT Symbol', 'File Creation Time')
    download_stock_companies_data_ftp(FTP_SERVER, FTP_FILE_PATH, DESTINATION_FILE)

    files = {features['data_symbol']: open(features['destination_file'], 'w+')
             for features in MARKETS.values()}

    with open(DESTINATION_FILE) as fp:
        for _, line in enumerate(fp):
            if line.startswith(lines_starts_to_ignore):
                continue
            data_symbol = line.split('|', maxsplit=3)[2]
            files[data_symbol].write(line)

    (file.close for file in files.values())


def get_stock_companies_symbols_tuples(market_name=None, from_file=False, file_path=None):
    if not from_file:
        download_markets_data()

    if file_path is None:
        file_path = MARKETS[market_name]['destination_file']

    return read_nasdaq_stock_companies_symbols_tuples_from_file(file_path)
