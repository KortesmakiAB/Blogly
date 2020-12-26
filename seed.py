from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
naomi = User(first_name='Naomi', last_name="Isagreat", img_url="https://media1.popsugar-assets.com/files/thumbor/qs5ImFjm0-zYcYGr7jevoWrd6FQ/0x151:2865x3016/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2020/04/29/822/n/1922398/c8c58cf95ea9cb29c20222.81553320_/i/Naomi-Campbell.jpg")
colt = User(first_name='Colt', last_name="Teachemup", img_url="https://pbs.twimg.com/profile_images/651500933050818560/fG3lG6kz_400x400.jpg")
spike = User(first_name='Spike', last_name="Porcupine")

# Add new objects to session, so they'll persist
db.session.add(naomi)
db.session.add(colt)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()
