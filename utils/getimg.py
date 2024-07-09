import pytesseract
from PIL import Image
import os
import configparser

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "../config/config.ini")
config.read(config_path)

ROTATION_ANGLES = list(map(int, config['ImageProcessing']['rotation_angles'].split(',')))

def get_inv_img(path, client):
    img = Image.open(path)
    for i in ROTATION_ANGLES:
        rotated_img = img.rotate(i)
        img_text = pytesseract.image_to_string(rotated_img)
        invoices_data = []

        if "invoice" in img_text.lower():
            with open(path, "rb") as f:
                poller = client.begin_analyze_document("prebuilt-invoice", document=f)
                result = poller.result()

            for document in result.documents:
                if document.doc_type == "invoice":
                    invoices_data.append(document)
            break 

    return invoices_data