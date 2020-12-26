from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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
    """TODO"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_form():
    """TODO"""

    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """TODO"""

    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url = request.form['i_url']
    if img_url == '':
        img_url = '/static/captainunderpants.png'
    
    new_user = User(first_name=f_name, last_name=l_name, img_url=img_url)
    # raise
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    """TODO"""

    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """TODO"""

    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """TODO"""

    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url = request.form['i_url']
    if img_url == '':
        img_url = '/static/captainunderpants.png'

    user = User.query.get_or_404(user_id)
    user.first_name = f_name
    user.last_name = l_name
    user.img_url = img_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """TODO"""

    User.query.filter_by(id = user_id).delete()
    db.session.commit()

    return redirect('/users')