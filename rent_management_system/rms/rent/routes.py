from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from rms import db
from rms.models import RentPayment
from rms.rent.forms import PayRentForm, RentForm

rent = Blueprint('rent', __name__)

@rent.route('/rent/new', methods=['GET','POST'])
@login_required
def add_rent():
    form = PayRentForm()
    if form.validate_on_submit():
        rent_payment = RentPayment(amount=form.amount.data, name=form.name.data, tenant=current_user)
        db.session.add(rent_payment)
        db.session.commit()

        flash('Your payment has been added successfully!', 'success')
        return redirect(url_for('main.rent'))

    return render_template('pay_rent.html', title='Add Rent Payment', form=form)

@rent.route('/rent/<int:rent_payment_id>')
def manage_rent(rent_payment_id):
     # Get the current user
    
    rent_payment = RentPayment.query.get_or_404(rent_payment_id)
    if rent_payment.tenant != current_user:
        abort(403)
        


    return render_template('manage.html', title='Manage Rent Payment', rent_payment=rent_payment , total_paid=total_paid, balance=balance)

@rent.route('/rent/<int:rent_payment_id>/update', methods=['GET', 'POST'])
@login_required
def update_rent(rent_payment_id):
    rent_payment = RentPayment.query.get_or_404(rent_payment_id)
    if rent_payment.tenant != current_user:
        abort(403)

    form = RentForm()
    if form.validate_on_submit():
        rent_payment.amount = form.amount.data
        rent_payment.name = form.name.data
        db.session.commit()

        flash('Your payment has been updated successfully!', 'success')
        return redirect(url_for('rent.manage_rent', rent_payment_id=rent_payment.id))

    elif request.method == 'GET':
        form.amount.data = rent_payment.amount
        form.name.data = rent_payment.name

    return render_template('rent.html', title='Update Rent Payment', form=form)

@rent.route('/rent/<int:rent_payment_id>/delete', methods=['POST'])
@login_required
def delete_rent(rent_payment_id):
    rent_payment = RentPayment.query.get_or_404(rent_payment_id)
    if rent_payment.tenant != current_user:
        abort(403)

    db.session.delete(rent_payment)
    db.session.commit()

    flash('Your payment has been deleted successfully!', 'success')
    return redirect(url_for('main.home'))
