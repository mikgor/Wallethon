import datetime
from decimal import Decimal

from PyPDF2 import PdfFileReader


def get_transactions_tuples_from_file(file_path):
    transactions_tuple_list = []

    with open(file_path, 'rb') as f:
        pdf = PdfFileReader(f)

        for page_num in range(pdf.getNumPages()):
            page = pdf.getPage(page_num).extractText()

            if 'Capacity' not in page or 'Net Amount' not in page:
                continue

            splitted_text = page.split('Capacity')[1].replace('$', '').split('Net Amount')[:-1]

            for transaction in splitted_text:
                line = transaction.split('\n')[::-1]
                other_fees = Decimal(line[1])
                transaction_fee = Decimal(line[3])
                commission = Decimal(line[5])
                date = datetime.datetime.strptime(line[12], '%m/%d/%Y').date()
                per_stock_price = Decimal(line[13])
                quantity = Decimal(line[14].replace('-', ''))
                type = line[15].upper()
                symbol = line[18]

                total_commission = commission + transaction_fee + other_fees

                transactions_tuple_list.append(
                    (symbol, type, quantity, per_stock_price, date, total_commission))

    return transactions_tuple_list


def get_transactions_tuples_from_files(files_paths):
    transactions_tuple_list = []

    for file_path in files_paths:
        for transaction in get_transactions_tuples_from_file(file_path):
            transactions_tuple_list.append(transaction)

    return transactions_tuple_list
