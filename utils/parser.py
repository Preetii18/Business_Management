import re
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# ---------- PDF and Image Text Extraction ---------- #

def extract_text_from_pdf(filepath):
    images = convert_from_path(
        filepath,
        poppler_path=r"C:\Users\vshpr\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    )
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def extract_text_from_image(filepath):
    image = Image.open(filepath)
    return pytesseract.image_to_string(image)

# ---------- Custom Extraction Helpers ---------- #

def extract_customer_name(text):
    lines = text.splitlines()
    customer_name = "Unknown"
    for i, line in enumerate(lines):
        if 'to:' in line.lower():
            # Option 1: name is after "To:" in the same line
            match = re.search(r'To:\s*(.*)', line, re.IGNORECASE)
            if match:
                return match.group(1).strip()

            # Option 2: name is on next line(s)
            for j in range(i + 1, i + 4):
                if j < len(lines) and lines[j].strip():
                    return lines[j].strip()
    return customer_name

def extract_amount(text, keyword):
    # Match variations like "Sub Total:", "Sub Total :", etc.
    pattern = rf"{keyword}[:\s]*₹?([\d,\.]+)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            amount_str = match.group(1).replace(",", "")
            return float(amount_str)
        except:
            return 0.0
    return 0.0

# ---------- Main Parsing Functions ---------- #

def parse_bill_pdf(filepath):
    text = extract_text_from_pdf(filepath)
    return extract_data_from_text(text)

def parse_bill_image(filepath):
    text = extract_text_from_image(filepath)
    return extract_data_from_text(text)

def extract_data_from_text(text):
    customer_name = extract_customer_name(text)
    subtotal = extract_amount(text, "Sub Total")
    total = extract_amount(text, "Total Amount") or extract_amount(text, "Grand Total")
    gst = total - subtotal if subtotal and total else 0.0

    return {
        "customer_name": customer_name,
        "subtotal": subtotal,
        "gst": gst,
        "total": total
    }
