import ftplib


def download_stock_companies_data_ftp(ftp_server, ftp_file_path, destination_file):
    ftp = ftplib.FTP(ftp_server)
    ftp.login()

    with open(destination_file, 'wb') as f:
        ftp.retrbinary('RETR ' + ftp_file_path, f.write)

    ftp.quit()


def read_nasdaq_stock_companies_symbols_tuples_from_file(file_path):
    lines_starts_to_ignore = ('Symbol', 'File Creation Time')
    companies_symbols_tuple_list = []

    with open(file_path) as fp:
        for _, line in enumerate(fp):
            if line.startswith(lines_starts_to_ignore):
                continue
            line_split = line.split('|', maxsplit=2)

            company_data = line_split[1].split('-', maxsplit=1)
            company_name = company_data[0].strip()
            company_details = company_data[1].strip() if len(company_data) > 1 else None

            companies_symbols_tuple_list.append(
                (line_split[0], company_name, company_details))

    return companies_symbols_tuple_list
