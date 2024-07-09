import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import configparser
from numbers_parser import Document

from utils.findinv import find_invoice_pg
from utils.emptyrow import find_empty_row
from utils.writeinv import write_invoices


config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config/config.ini")
config.read(config_path)


ENDPOINT = config['Azure']['endpoint']
KEY = config['Azure']['api_key']
INV_PATH = config['Paths']['invoice_path']
SHEET = config['Paths']['invo_sheet']
INVOICE_FIELDS = config['InvoiceFields']['fields'].split(',')

def main():

    endpoint = ENDPOINT
    api_key = KEY

    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    invoice_path = INV_PATH
    invo_sheet = SHEET

    invoices_data = find_invoice_pg(invoice_path, document_analysis_client)

    doc = Document("invoices.numbers")
    sheets = doc.sheets
    tables = sheets[0].tables
    table = tables[0]

    empty_row = None
    empty_row = find_empty_row(table, INVOICE_FIELDS)

    if empty_row == 0:
        for col_num, header in enumerate(INVOICE_FIELDS):
            table.write(0, col_num, header)
        empty_row += 1

    write_invoices(invoices_data, table, empty_row)

    doc.save(invo_sheet)
    print("done")

if __name__ == "__main__":
    main()