import tempfile
import fitz
import io
import concurrent.futures

from utils.findimg import extract_text_from_image


def getinvpg(doc, page):
    inv_pgs = []


    return inv_pgs

def process_page(doc, page, pg_num, client):
    all_invoices = []
    invoices_data = []
    text = page.get_text()

    if "invoice" in text.lower():
        temp_pdf_path = tempfile.mktemp(suffix=".pdf")
        doc_part = fitz.open()
        doc_part.insert_pdf(doc, from_page=pg_num, to_page=pg_num)
        doc_part.save(temp_pdf_path)

        with open(temp_pdf_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-invoice", document=f)
            result = poller.result()

        for document in result.documents:
            if document.doc_type == "invoice":
                invoices_data.append(document)
                all_invoices.append(pg_num)

    images = page.get_images(full=True)
    for img_idx, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        
        img_stream = io.BytesIO(image_bytes)
        ls = [0, 90, 180, 360]
        for i in ls:
            img_text = extract_text_from_image(img_stream, i)
            if "invoice" in img_text.lower():
                img_stream.seek(0)
                poller = client.begin_analyze_document("prebuilt-invoice", document=img_stream)
                result = poller.result()

                for document in result.documents:
                    if document.doc_type == "invoice":
                        invoices_data.append(document)
                        all_invoices.append(pg_num)
                break

    return all_invoices, invoices_data

def find_invoice_pg(pdf_path, client):
    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    all_invoices = []
    invoices_data = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for pg_num in range(num_pages):
            page = doc.load_page(pg_num)
            futures.append(executor.submit(process_page, doc, page, pg_num, client))

        for future in concurrent.futures.as_completed(futures):
            invoices, data = future.result()
            all_invoices.extend(invoices)
            invoices_data.extend(data)

    doc.close()
    return all_invoices, invoices_data
