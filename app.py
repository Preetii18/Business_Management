from flask import Flask, request, render_template, redirect, url_for
import os
from utils.parser import parse_bill_pdf, parse_bill_image 
from models import db, Bill
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Uploads and config
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/business.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/dashboard')
def dashboard():
    # Placeholder values — connect to real data later
    total_sales = 5
    total_purchases = 3
    labels = ['Jan', 'Feb', 'Mar']
    sales_data = [10000, 12000, 9000]
    purchase_data = [8000, 11000, 7500]

    return render_template('dashboard.html',
                           total_sales=total_sales,
                           total_purchases=total_purchases,
                           labels=labels,
                           sales_data=sales_data,
                           purchase_data=purchase_data)


# Optional redirect from home page
@app.route('/')
def home():
    return redirect(url_for('upload_bill'))

# Upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_bill():
    if request.method == 'POST':
        file = request.files['file']
        bill_type = request.form.get('type')  # "sale" or "purchase"

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Parse bill content
        if filename.lower().endswith('.pdf'):
            data = parse_bill_pdf(filepath)
        else:
            data = parse_bill_image(filepath)

        # Show extracted data on same page
        return render_template('upload.html', data=data, bill_type=bill_type)

    # GET method: show form
    return render_template('upload.html')

# Start the server
if __name__ == '__main__':
    app.run(debug=True)


