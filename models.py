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
                   primary_key=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    img_url = db.Column(db.String(555),
                        default = 'https://www.baltimoresun.com/resizer/sESny2X0OQREJK5HFvv0k3sh9DA=/415x383/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/YLOX2SB7L5BOXAM742HV427NK4.jpg')

    def __repr__(self):
        """Show info about User"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.img_url}>"

class Post(db.Model):
    """Post Class"""

    __tablename__ = "posts"

    id          = db.Column(db.Integer,
                            primary_key = True)
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


class Tag(db.Model):
    """Tag Model"""

    __tablename__ = 'tags'

    id      = db.Column(db.Integer,
                        primary_key = True)
    name    = db.Column(db.String(50),
                        unique = True,
                        nullable = False)

    posts   = db.relationship('Post',
                            secondary = 'poststags',
                            backref = 'tagged_words')

    def __repr__ (self):
        """Show information about Tag instances"""

        return f'<Post {self.id} {self.name}>'


class PostTag(db.Model):
    """joins Post and Tag"""

    __tablename__ = 'poststags'

    post    = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True,
                        nullable = False)
    tag     = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key = True,
                        nullable = False)