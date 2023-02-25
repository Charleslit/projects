from flask import render_template, request
from datetime import datetime


@app.route('/tenants/<int:id>/pay-rent', methods=['GET', 'POST'])
def pay_rent(id):
    tenant = Tenant.query.get(id)
    if request.method == 'POST':
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        payment = RentPayment(amount=amount, date=date, tenant=tenant)
        db.session.add(payment)
        db.session.commit()
        return 'Payment successful!'
    return render_template('pay_rent.html', tenant=tenant)