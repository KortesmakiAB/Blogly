from flask import Flask, request, redirect, render_template
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """TODO"""

    return redirect('/users')

@app.route('/users')
def display_users():
    """Display a list of users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Display a form to add a new user"""

    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Add new user to users table"""

    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url = request.form['i_url']
    if img_url == '':
        img_url = 'https://www.baltimoresun.com/resizer/sESny2X0OQREJK5HFvv0k3sh9DA=/415x383/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/YLOX2SB7L5BOXAM742HV427NK4.jpg'
        # img_url = 'https://static.wikia.nocookie.net/captainunderpants/images/c/c1/Capt-character-captainunderpants.png/revision/latest?cb=20200503124947'
        # img_url = 'https://static.wikia.nocookie.net/captainunderpants/images/8/83/Capt-character-captainunderpants.jpg/revision/latest/scale-to-width-down/300?cb=20180714224749'
    
    new_user = User(first_name=f_name, last_name=l_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    """Display user details"""

    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Display user info. Allow user info to be edited"""

    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Update users table with edited user info"""

    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url = request.form['i_url']
    if img_url == '':
        img_url = 'https://www.baltimoresun.com/resizer/sESny2X0OQREJK5HFvv0k3sh9DA=/415x383/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/YLOX2SB7L5BOXAM742HV427NK4.jpg'
        # img_url = 'https://static.wikia.nocookie.net/captainunderpants/images/c/c1/Capt-character-captainunderpants.png/revision/latest?cb=20200503124947'
        # img_url = 'https://static.wikia.nocookie.net/captainunderpants/images/8/83/Capt-character-captainunderpants.jpg/revision/latest/scale-to-width-down/300?cb=20180714224749'

    user = User.query.get_or_404(user_id)
    user.first_name = f_name
    user.last_name = l_name
    user.img_url = img_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user from users table"""

    User.query.filter_by(id = user_id).delete()
    db.session.commit()

    return redirect('/users')