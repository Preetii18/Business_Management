import re
import pytesseract
from PIL import Image
from pdfminer.high_level import extract_text

def parse_bill_pdf(path):
    text = extract_text(path)
    return extract_data_from_text(text)

def parse_bill_image(path):
    text = pytesseract.image_to_string(Image.open(path))
    return extract_data_from_text(text)

def extract_data_from_text(text):
    subtotal = search_keyword(r'Sub\s*Total[:\s]+([\d,\.]+)', text)
    grandtotal = search_keyword(r'Grand\s*Total\s*INR[:\s]+([\d,\.]+)', text)

    return {
        "sub total": subtotal,
        "grand total": grandtotal,
    }

def search_keyword(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return float(match.group(1).replace(',', ''))
    return None

