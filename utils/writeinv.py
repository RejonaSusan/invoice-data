import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "../config/config.ini")
config.read(config_path)

INVOICE_FIELDS = config['InvoiceFields']['fields'].split(',')

def write_invoices(invoices_data, table, empty_row):
    for idx, invoice in enumerate(invoices_data):
        row = []
        for field in INVOICE_FIELDS:
            field_value = invoice.fields.get(field)
            row.append(field_value.value if field_value else "")
        for col_num, value in enumerate(row):
            table.write(empty_row, col_num, str(value))
        empty_row += 1
