from flask import Blueprint, render_template, request
from rms.models import Post, User, RentPayment

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/Home")
def Home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('Home.html', posts=posts)

@main.route('/About')
def about():
    users = RentPayment.query.all()
    return render_template('About.html', title='About', users = users)

@main.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', title='users', users=users)


@main.route('/rent')
def rent():
    users = User.query.all()
    rent_info = []
    for user in users:
        latest_rent_payment = RentPayment.query.filter_by(tenant_id=user.id).order_by(RentPayment.date.desc()).first()
        balance = user.get_rent_balance(rent_amount=latest_rent_payment.amount if latest_rent_payment else 0)
        total_rent_paid = user.get_total_rent_paid()
        rent_info.append({'user': user, 'latest_rent_payment': latest_rent_payment, 'balance':balance,'total_rent_paid': total_rent_paid})
    return render_template('rent.html', title='Rent', rent_info=rent_info)
