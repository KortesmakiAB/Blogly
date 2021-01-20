from flask import Flask, request, redirect, render_template
from models import *
import os 
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'PssssssssstPleaseDoNOOOOTTEll')

connect_db(app)

debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """Display Homepage"""

    return render_template('index.html')

@app.route('/users')
def display_users():
    """Display a list of users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Display a form to add a new user"""

    return render_template('user_new.html')

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

    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Display user info. Allow user info to be edited"""

    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html', user=user)

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

###########################################################
# "posts" Routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """For the selected user, show form to add a post."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('post_new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_add_post_form(user_id):
    """Add post and redirect to the user detail page"""

    # Naomi: I am still not quite sure what it looks like to write server side form vaidation. 
    # How does this look??
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.getlist('cb')
    except:
        return "invalid new post data submission"
    
    new_post = Post(title=title, content=content, user=user_id)

    for tag in tags:
        tag_from_form = db.session.query(Tag).filter_by(name = tag).one()
        new_post.tagged_words.append(tag_from_form)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def display_post(post_id):
    """Show a post.
    Show buttons to edit and delete the post.
    Show tags which are also links to the tag details."""

    post = Post.query.get(post_id)

    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def handle_edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post_edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    title = request.form['title']
    content = request.form['content']
    
    p = Post.query.get(post_id)
    p.title = title
    p.content = content

    tags = request.form.getlist('cb')
    for tag in tags:
        tag_from_form = db.session.query(Tag).filter_by(name = tag).one()
        p.tagged_words.append(tag_from_form)

    db.session.add(p)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post. Redirect to user view"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user

    Post.query.filter_by(id = post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')

###########################################################
# "tag" Routes

@app.route('/tags')
def display_tags():
    """Lists all tags, with links to the tag detail page"""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""

    tag = db.session.query(Tag).get_or_404(tag_id)
    # or
    # tag = Tag.query.get_or_404(tag_id)

    return render_template('tags_details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show edit form for a tag."""

    tag = db.session.query(Tag).get_or_404(tag_id)

    return render_template('tags_edit.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_tag_edit(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = db.session.query(Tag).get_or_404(tag_id)
    t_name = request.form['t_name']
    tag.name = t_name

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/new')
def tag_form():
    """Shows a form to add a new tag."""

    return render_template('tags_new.html')


@app.route('/tags/new', methods=['POST'])
def handle_tag_post():
    """Process add form, adds tag, and redirect to tag list."""

    t_name = request.form['t_name']
    new_tag = Tag(name = t_name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag and redirect to tag list"""

    db.session.query(Tag).filter_by(id = tag_id).delete()
    # or
    # Tag.query.filter_by(id = tag_id).delete()
    db.session.commit()

    return redirect('/tags')
