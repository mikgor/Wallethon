import ftplib

FTP_SERVER = 'ftp.nasdaqtrader.com'
FTP_FILE_PATH = 'SymbolDirectory/nasdaqlisted.txt'
DESTINATION_FILE_NAME = 'apps/stocks/utils/data/nasdaq_stocks.txt'


def download_stock_companies_data():
    ftp = ftplib.FTP(FTP_SERVER)
    ftp.login()

    with open(DESTINATION_FILE_NAME, 'wb') as f:
        ftp.retrbinary('RETR ' + FTP_FILE_PATH, f.write)

    ftp.quit()


def get_stock_companies_symbols_tuples(from_file=False, file_path=None):
    companies_symbols_tuple_list = []
    lines_starts_to_ignore = ('Symbol', 'File Creation Time')

    if file_path is None:
        file_path = DESTINATION_FILE_NAME

    if not from_file:
        download_stock_companies_data()

    with open(file_path) as fp:
        for _, line in enumerate(fp):
            if line.startswith(lines_starts_to_ignore):
                continue
            line_split = line.split('|', maxsplit=2)
            companies_symbols_tuple_list.append((line_split[0], line_split[1]))

    return companies_symbols_tuple_list
