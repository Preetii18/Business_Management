new_bill = Bill(
    filename=filename,
    bill_type=bill_type,
    subtotal=data.get("Sub Total"),
    total=data.get("Total"),
    customer_name=data.get("Customer Name")
)
db.session.add(new_bill)
db.session.commit()
