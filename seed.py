from models import User, db, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
naomi = User(first_name='Naomi', last_name="Isgreat", img_url="https://media1.popsugar-assets.com/files/thumbor/qs5ImFjm0-zYcYGr7jevoWrd6FQ/0x151:2865x3016/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2020/04/29/822/n/1922398/c8c58cf95ea9cb29c20222.81553320_/i/Naomi-Campbell.jpg")
colt = User(first_name='Colt', last_name="Teachemup", img_url="https://pbs.twimg.com/profile_images/651500933050818560/fG3lG6kz_400x400.jpg")

db.session.add_all([naomi, colt])
db.session.commit()

# Add posts
naomi_p1 = Post(title='Happy New Year', user=1, content="For auld lang syne, my dear, For auld lang syne, We'll tak a cup o' kindness yet, For days of auld lang syne")
naomi_p2 = Post(title='Learning more', user=1, content='Mostly, you need to learn principles, which are more important than individual technologies.')
colt_p1 = Post(title="Chickens, the more you know...", user=2, content="Naming chickens is my single greatest skill, it is my legacy.")

db.session.add_all([naomi_p1, naomi_p2, colt_p1])
db.session.commit()

# Add tags
noice       = Tag(name = 'noice')
inspiration = Tag(name = 'inspiration')
sorry       = Tag(name = 'sorry-not-sorry')

db.session.add_all([noice, inspiration, sorry])
db.session.commit()

# Add poststags
pt1 = PostTag(post = 2, tag = 2)
pt2 = PostTag(post = 1, tag = 1)
pt3 = PostTag(post = 3, tag = 3)
pt4 = PostTag(post = 3, tag = 2)

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()