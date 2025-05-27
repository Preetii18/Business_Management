from flask import Flask, request, jsonify, render_template
import os
from utils.parser import parse_bill_pdf, parse_bill_image
from models import db, Customer, Sale, Purchase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/upload', methods=['POST'])
def upload_bill():
    file = request.files['file']
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    if filename.endswith('.pdf'):
        data = parse_bill_pdf(filepath)
    else:
        data = parse_bill_image(filepath)

    # For demo: hardcoded customer name (we’ll extract later)
    customer_name = request.form.get('customer') or 'Unknown Customer'

    # Find or create customer
    customer = Customer.query.filter_by(name=customer_name).first()
    if not customer:
        customer = Customer(name=customer_name)
        db.session.add(customer)
        db.session.commit()

    # Save sale record
    sale = Sale(
        subtotal=data.get('subtotal'),
        gst=data.get('gst'),
        total=data.get('total'),
        customer=customer
    )
    db.session.add(sale)

    # Update customer total
    customer.total_purchase += data.get('total') or 0.0

    db.session.commit()

    return jsonify(data)

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)


