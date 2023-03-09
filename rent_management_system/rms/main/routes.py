from flask import Blueprint, render_template, request
from rms.models import Post, User, RentPayment, Room
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
@main.route('/manage')
def manage():
    
    rent_h = RentPayment.query.all()
    return render_template('manage.html', rent_h=rent_h)
  

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
@main.route('/rooms', methods=['GET', 'POST'])
def rooms():
    # Get all the rooms
    rooms = Room.query.all()

    # Get the number of occupied, vacant, and booked rooms
    occupied_count = Room.query.filter_by(status='occupied').count()
    vacant_count = Room.query.filter_by(status='vacant').count()
    booked_count = Room.query.filter_by(status='booked').count()

    # Check if the form has been submitted
    if request.method == 'POST':
        # Get the form data
        room_number = request.form['room_number']
        check_in = datetime.strptime(request.form['check_in'], '%Y-%m-%d')
        check_out = datetime.strptime(request.form['check_out'], '%Y-%m-%d')

        # Check if the room is available for booking
        room = Room.query.filter_by(room_number=room_number).first()
        if room.status != 'vacant':
            flash('This room is not available for booking.', 'danger')
            return redirect(url_for('rooms'))

        # Create a new booking
        booking = Booking(room_id=room.id, check_in=check_in, check_out=check_out)

        # Update the room status to booked
        room.status = 'booked'

        # Add the booking and room status changes to the database
        db.session.add(booking)
        db.session.commit()

        # Flash a success message and redirect to the rooms page
        flash('Your booking has been confirmed!', 'success')
        return redirect(url_for('rooms'))

    # Render the template with the room data and counts
    return render_template('rooms.html', rooms=rooms, occupied_count=occupied_count, vacant_count=vacant_count, booked_count=booked_count)
