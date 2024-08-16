import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import configparser
import openpyxl
import fitz
from PIL import Image

from utils.findinv import get_invoice_pg
from utils.emptyrow import find_empty_row
from utils.writeinv import write_invoices
from utils.getimg import get_inv_img

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config/config.ini")
config.read(config_path)

ENDPOINT = config['Azure']['endpoint']
KEY = config['Azure']['api_key']
INV_PATH = config['Paths']['invoice_path']
SHEET = config['Paths']['invo_sheet']
INVOICE_FIELDS = config['InvoiceFields']['fields'].split(',')

def is_pdf(file_path):
    ext = file_path.split('.')[-1]
    return ext == "pdf"


def main():

    endpoint = ENDPOINT
    api_key = KEY

    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    invoice_path = INV_PATH
    invo_sheet = SHEET

    if is_pdf(invoice_path):
        invoices_data = get_invoice_pg(invoice_path, document_analysis_client, pages=3)
    else:
        invoices_data = get_inv_img(invoice_path, document_analysis_client)

    wb = openpyxl.load_workbook(invo_sheet)
    sheet = wb.active
    sheet.title = "Invoice-sheet"

    empty_row = find_empty_row(sheet, INVOICE_FIELDS)
    write_invoices(invoices_data, sheet, empty_row)

    wb.save(invo_sheet)
    print("Done")

if __name__ == "__main__":
    main()
