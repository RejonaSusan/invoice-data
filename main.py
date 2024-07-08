import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from numbers_parser import Document
from utils.findinv import find_invoice_pg
from utils.emptyrow import find_empty_row
from utils.writeinv import write_invoices

load_dotenv()

def main():

    endpoint = os.getenv("endpoint")
    api_key = os.getenv("api_key")

    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    invoice_path = "/Users/rejonasusan/Downloads/jpginve (1)_merged_merged.pdf"
    invo_sheet = "/Users/rejonasusan/Desktop/HPE/invo/invoices.numbers"

    invoices, invoices_data = find_invoice_pg(invoice_path, document_analysis_client)

    if not invoices:
        print("No invoices found in the document")
    else:
        print(f"Invoices found on pages: {invoices}")

    headers = ["Vendor Name", "Invoice Id", "Invoice Date", "Total Due"]

    doc = Document("invoices.numbers")
    sheets = doc.sheets
    tables = sheets[0].tables
    table = tables[0]

    empty_row = None
    empty_row = find_empty_row(table, headers)

    if empty_row == 0:
        for col_num, header in enumerate(headers):
            table.write(0, col_num, header)
        empty_row += 1

    write_invoices(invoices_data, table, empty_row)

    doc.save(invo_sheet)
    print("done")

if __name__ == "__main__":
    main()