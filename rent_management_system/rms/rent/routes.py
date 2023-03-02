from flask import Blueprint , render_template, url_for, flash, redirect, request
from  flask import (render_template, url_for, flash, redirect, request, abort, )
from flask_login import current_user, login_required
from rms import db
from rms.models import RentPayment
from rms.rent.forms import PayRentForm



rent = Blueprint('rent', __name__)



@rent.route('/rent/new' ,methods=['GET','POST'])
@login_required
def add_pay():
    form = PayRentForm()
    if form.validate_on_submit():
      rent = RentPayment(amount= form.amount.data, name = form.name.data, tenant = current_user)
      db.session.add(rent)
      db.session.commit()

      flash('your payment has been added added ', 'success')
      return redirect(url_for('main.Home'))
    return render_template('pay_rent.html', title='add_pay' , form = form , legend = add_pay ) 
    
@rent.route('/rent/<int:rent_payments_id>')
def rents(rent_payments_id):
        rent_payments = RentPayment.query.get_or_404(rent_payments_id)
        return render_template('manage.html',title='mange_account', rent=rent )

@rent.route('/rent/<int:rent_payments_id>/update', methods=['GET','POST'] )
@login_required
def update_pay(rent_payments_id):
            rent_payments = RentPayment.query.get_or_404(rent_payments_id)
            if rent.tenant != current_user:
             abort(403)
            form = RentForm()
            if form.validate_on_submit():
                  rent.amount = form.amount.data
                  rent.name = form.name.data
                  db.session.commit()
                  flash('your payment has been updated', 'success')
                  return redirect(url_for('rent.rents',rent_payments_id = rents.id))
            elif request.method == 'GET':
             
             form.amount.data =rent.amount
             form.name.data = rent.name

            return render_template('rent.html',title='update pay',form = form, legend = update_payment )

@rent.route('/rent/<int:rent_payments_id>/delete', methods=['POST'] )
@login_required
def delete_payment(rent_payments_id):
      rent = RentPayment.query.get_or_404(rent_payments_id)
      if rent.tenant != current_user:
            abort(403)
      db.session.delete(rent)
      db.session.commit()
      flash('your post has been deleted !', 'success') 
      return redirect(url_for('main.Home'))     


      
