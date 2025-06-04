import re
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Extract text from PDF
def extract_text_from_pdf(filepath):
    images = convert_from_path(filepath)
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

# Extract text from Image
def extract_text_from_image(filepath):
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image)
    return text

# Extract customer name after 'To'
def extract_customer_name(text):
    lines = text.splitlines()
    customer_name = "Unknown"
    for i, line in enumerate(lines):
        if re.search(r'\bTo\b', line, re.IGNORECASE):
            for j in range(i + 1, i + 4):
                if j < len(lines) and lines[j].strip():
                    customer_name = lines[j].strip()
                    return customer_name
    return customer_name

# Extract amount after keyword (e.g., Sub Total, Grand Total)
def extract_amount(text, keyword):
    match = re.search(rf"{keyword}[:\s]*([\d,]+)", text, re.IGNORECASE)
    if match:
        amount_str = match.group(1).replace(",", "")
        return int(amount_str)
    return 0

# Main parser for PDF
def parse_bill_pdf(filepath):
    text = extract_text_from_pdf(filepath)
    return extract_data_from_text(text)

# Main parser for Image
def parse_bill_image(filepath):
    text = extract_text_from_image(filepath)
    return extract_data_from_text(text)

# Extract final structured data
def extract_data_from_text(text):
    customer_name = extract_customer_name(text)
    subtotal = extract_amount(text, "Sub Total")
    total = extract_amount(text, "Grand Total")
    gst = total - subtotal if subtotal and total else 0

    return {
        "customer_name": customer_name,
        "subtotal": subtotal,
        "gst": gst,
        "total": total
    }

def extract_text_from_pdf(filepath):
    images = convert_from_path(
        filepath,
        poppler_path=r"C:\Users\vshpr\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    )
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image)
    return text




