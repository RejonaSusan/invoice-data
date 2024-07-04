import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from numbers_parser import Document
import PyPDF2
from PyPDF2 import PdfWriter
import tempfile
from PIL import Image

load_dotenv()

endpoint = os.getenv("endpoint")
api_key = os.getenv("api_key")

document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

invoice_path = "/Users/rejonasusan/Downloads/sampleinv.png"
invo_sheet = "/Users/rejonasusan/Desktop/HPE/invo/invoices.numbers"

def is_image(file_path):
    try:
        Image.open(file_path)
        return True
    except IOError:
        return False

def find_invoice_pages_in_pdf(pdf_path, client):
    invoice_pages = []
    reader = PyPDF2.PdfReader(pdf_path)
    num_pages = len(reader.pages)

    for page_number in range(num_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number])
        temp_pdf_path = tempfile.mktemp(suffix=".pdf")
        with open(temp_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        with open(temp_pdf_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-invoice", document=f)
            result = poller.result()

        if result.documents:
            for document in result.documents:
                if document.doc_type == "invoice":
                    invoice_pages.append(page_number + 1)
                    break

    return invoice_pages

def find_invoice_pages(file_path, client):
    if is_image(file_path):
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-invoice", document=f)
            result = poller.result()
        return [1] if result.documents else []
    else:
        return find_invoice_pages_in_pdf(file_path, client)

invoice_pages = find_invoice_pages(invoice_path, document_analysis_client)
if not invoice_pages:
    print("No invoices found in the document")
else:
    print(f"Invoices found on pages: {invoice_pages}")

invoices_data = []
if is_image(invoice_path):
    with open(invoice_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", document=f)
        result = poller.result()
    invoices_data.extend(result.documents)
else:
    for page_number in invoice_pages:
        writer = PdfWriter()
        reader = PyPDF2.PdfReader(invoice_path)
        writer.add_page(reader.pages[page_number - 1])
        temp_pdf_path = tempfile.mktemp(suffix=".pdf")
        with open(temp_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        with open(temp_pdf_path, "rb") as f:
            poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", document=f)
            result = poller.result()
        invoices_data.extend(result.documents)

with open(invoice_path, "rb") as f:
    invoice = f.read()

def is_row_empty(table, row_index):
    for col_index in range(table.num_cols):
        cell = table.cell(row_index, col_index)
        if cell and cell.value:
            return False
    return True

headers = ["Vendor Name", "Invoice Id", "Invoice Date", "Total Due"]

doc = Document(invo_sheet)
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


for idx, invoice in enumerate(invoices_data):
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
    invoice_total = invoice.fields.get("InvoiceTotal")
    if total_due or invoice_total:
        row.append(total_due.value if (total_due or invoice_total) else "")

    for col_num, value in enumerate(row):
        table.write(empty_row, col_num, str(value))
    empty_row += 1

doc.save(invo_sheet)
print("done")
