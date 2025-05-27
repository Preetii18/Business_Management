# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy instance here
db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    total_purchase = db.Column(db.Float, default=0.0)

    sales = db.relationship('Sale', backref='customer', lazy=True)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    subtotal = db.Column(db.Float)
    gst = db.Column(db.Float)
    total = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    subtotal = db.Column(db.Float)
    gst = db.Column(db.Float)
    total = db.Column(db.Float)
