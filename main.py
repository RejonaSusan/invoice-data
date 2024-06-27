import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from numbers_parser import Document

load_dotenv()

endpoint = os.getenv("endpoint")
api_key = os.getenv("api_key")

document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

invoice_path = "/Users/rejonasusan/Downloads/inv1.pdf"
invo_sheet = "/Users/rejonasusan/Desktop/HPE/invo/invoices.numbers"

with open(invoice_path, "rb") as f:
    invoice = f.read()

poller = document_analysis_client.begin_analyze_document(model_id="prebuilt-invoice", document=invoice)
invoices = poller.result()

def is_row_empty(table, row_index):
    for col_index in range(table.num_cols):
        cell = table.cell(row_index, col_index)
        if cell and cell.value:
            return False
    return True

headers = ["Vendor Name", "Invoice Id", "Invoice Date", "Total Due"]

doc = Document("invoices.numbers")
sheets = doc.sheets
tables = sheets[0].tables
table = tables[0]
rows = table.rows()

empty_row = None
for i in range(len(rows)):
    if is_row_empty(table, i):
        empty_row = i
        break

if empty_row is None:
    empty_row = table.num_rows

if empty_row == 0:
    for col_num, header in enumerate(headers):
        table.write(0, col_num, header)
    empty_row += 1

for idx, invoice in enumerate(invoices.documents):
    row = []
    vendor_name = invoice.fields.get("VendorName")
    if vendor_name:
        row.append(vendor_name.value if vendor_name else "")
    invoice_id = invoice.fields.get("InvoiceId")
    if invoice_id:
        row.append(invoice_id.value if invoice_id else "")

    invoice_date = invoice.fields.get("InvoiceDate")
    if invoice_date:
        row.append(invoice_date.value if invoice_date else "")

    total_due = invoice.fields.get("AmountDue")
    if total_due:
        row.append(total_due.value if total_due else "")
    
    invoice_total = invoice.fields.get("InvoiceTotal")
    if invoice_total:
        row.append(invoice_total.value if vendor_name else "")

    for col_num, value in enumerate(row):
        table.write(empty_row, col_num, str(value))
    empty_row += 1

doc.save(invo_sheet)
print("done")

