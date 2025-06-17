# Business Management System 🧾📊

A Flask-based web application that allows businesses to upload bills/invoices (PDF/Image) and automatically extract key details like:

- Customer Name (from "To:" section)
- Sub Total
- Grand Total
- GST

### 🚀 Features
- Upload and parse scanned invoices or PDFs
- Extract total, subtotal, GST
- Detect customer name from "To:" section
- Simple UI for uploads (HTML, CSS, JS)

### 🛠️ Tech Stack
- Python, Flask
- HTML/CSS/JS (UI)
- Tesseract OCR
- pdf2image, pytesseract, OpenCV

### 📌 Status
⚠️ This project is **in progress** and under active development. More features like dashboard, data analytics, and database integration coming soon!

---

### 📂 Setup
1. Clone the repo:
   ```bash
   git clone https://github.com/Preetii18/Business_Management.git
   cd Business_Management
   
2. Install dependencies:
  pip install -r requirements.txt

4. Run the app:
  python app.py
