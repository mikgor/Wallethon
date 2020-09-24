import datetime
from urllib.request import urlopen

from lxml import etree

DESTINATION_FILE_NAME = 'apps/stocks/transactions/utils/data/stock_splits.txt'


def download_stock_splits_data(day: str):
    url = f'https://finance.yahoo.com/calendar/splits?day={day}'
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)

    symbols = tree.xpath("(//td[@aria-label='Symbol']//a/text())")
    companies = tree.xpath("(//td[@aria-label='Company']/text())")
    pay_dates = tree.xpath("(//td[@aria-label='Payable on']/span/text())")
    optionals = tree.xpath("(//td[@aria-label='Optionable?']/text())")
    ratios = tree.xpath("(//td[@aria-label='Ratio']/text())")

    with open(DESTINATION_FILE_NAME, 'a+') as fp:
        for index, symbol in enumerate(symbols):
            company = companies[index]
            pay_date = datetime.datetime.strptime(pay_dates[index], '%b %d, %Y')
            optional = optionals[index]
            ratio = ratios[index]
            fp.write(f"\n{symbol}|{company}|{pay_date}|{optional}|{ratio}")


def get_stock_splits_tuples(file_path=None):
    stock_splits_tuple_list = []
    lines_starts_to_ignore = ('Symbol',)

    if file_path is None:
        file_path = DESTINATION_FILE_NAME

    with open(file_path) as fp:
        for _, line in enumerate(fp):
            if line.startswith(lines_starts_to_ignore):
                continue
            line_split = line.split('|', maxsplit=5)

            symbol = line_split[0]
            pay_date = datetime.datetime.strptime(line_split[2], '%Y-%m-%d').date()
            optional = True if line_split[3] == 'T' else False
            ratio = line_split[4].strip().split(' - ')

            if len(ratio) == 2:
                ratio_from = float(ratio[0])
                ratio_for = float(ratio[1])

                stock_splits_tuple_list.append(
                    (symbol, pay_date, optional, ratio_from, ratio_for))

    return stock_splits_tuple_list
