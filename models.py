# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# ===========================
# Customer Table
# ===========================
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(15), nullable=True)

    total_purchase = db.Column(db.Float, default=0.0)

    # Relationships
    sales = db.relationship('Sale', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"

# ===========================
# Sales Table
# ===========================
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    subtotal = db.Column(db.Float, nullable=False)
    gst = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)

    def __repr__(self):
        return f"<Sale {self.id} - ₹{self.total}>"

# ===========================
# Purchases Table
# ===========================
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    subtotal = db.Column(db.Float, nullable=False)
    gst = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Purchase {self.id} - ₹{self.total}>"

# ===========================
# OPTIONAL FUTURE: Bill Items Table
# ===========================
# If you want to track itemized products/services:
# class BillItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     bill_type = db.Column(db.String(10))  # 'sale' or 'purchase'
#     description = db.Column(db.String(255))
#     quantity = db.Column(db.Integer)
#     price = db.Column(db.Float)
#     total = db.Column(db.Float)
#     bill_id = db.Column(db.Integer)  # Link to Sale or Purchase ID
