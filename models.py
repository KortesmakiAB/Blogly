from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    img_url = db.Column(db.String(555))

    def __repr__(self):
        """Show info about User"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.img_url}>"

class Post(db.Model):
    """Post Class"""

    __tablename__ = "posts"

    id          = db.Column(db.Integer,
                            primary_key = True)
                            # autoincrement = True)
    title       = db.Column(db.String(50),
                            nullable = False)
    content     = db.Column(db.String(500),
                            nullable = False)
    created_at  = db.Column(db.DateTime, 
                            nullable = False,
                            default = datetime.datetime.now)
    user        = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            nullable = False)

    user_details       = db.relationship('User', backref='posts')

    def __repr__(self):
        """Show information about Post instances"""

        p = self
        return f'<Post {p.id} {p.title} {p.content} {p.created_at}>'


