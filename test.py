import PyPDF2

def test_pdf_reading(pdf_path):
    try:
        file = open(pdf_path, 'rb')
        reader = PyPDF2.PdfReader(file)
        
        num_pages = len(reader.pages)
        print(f"Total pages in PDF: {num_pages}")
        
        for page_number in range(num_pages):
            print(f"Page number: {page_number}")
        
        file.close()
    except Exception as e:
        print(f"An error occurred: {e}")


pdf_path = "/Users/rejonasusan/Downloads/jpginve (1)_merged.pdf"
test_pdf_reading(pdf_path)
