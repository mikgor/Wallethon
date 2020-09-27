DESTINATION_FILE_NAME = 'apps/stocks/markets/utils/data/gpw_stocks.txt'


def get_stock_companies_symbols_tuples(file_path=None):
    companies_symbols_tuple_list = []
    lines_starts_to_ignore = ('Main Market',)

    if file_path is None:
        file_path = DESTINATION_FILE_NAME

    with open(file_path, encoding='utf8') as fp:
        for _, line in enumerate(fp):
            if line.startswith(lines_starts_to_ignore):
                continue
            line_split = line.split('(')
            companies_symbols_tuple_list.append((line_split[1].split(')')[0], line_split[0].strip(), None))

    return companies_symbols_tuple_list
