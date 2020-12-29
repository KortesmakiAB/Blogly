from unittest import TestCase
from app import app
from models import *

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# start test db from scratch each time we run this file
db.drop_all()
db.create_all()


class BloglyFlaskTests(TestCase):
    """Unittests for Blogly Flask Routes"""

    def setUp(self):
        """Before each test..."""
        
        # Make Flask errors be real errors, not HTML pages with error info.
        # Stop flask debug toolbar from running and interfering with tests (This is a bit of a hack)"""
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

        User.query.delete()
    
    def tearDown(self):
        """After each test..."""

        db.session.rollback()

    def test_base_and_users_html(self):
        """Test for status code at users.html. Test for html in base.html and users.html"""

        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text='True')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"', html)
            self.assertIn('<button type="submit" class="btn btn-primary">Add User</button>', html)

    def test_add_user_form_html(self):
        """Test add new user form page for status code and html in new_user.html"""

        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/users/new" method="POST">', html)
            self.assertIn('First Name</label>', html)

    def test_add_user_redirect(self):
        """Test redirect on POST route for new user form submission"""

        with app.test_client() as client:
            new_user = {'f_name':'John', 'l_name':'Doe', 'i_url':''}
            resp = client.post('/users/new', data=new_user)

            self.assertEqual(resp.status_code, 302)

    def test_add_user_form_post(self):
        """Test if new_user data is displayed on redirect to /users after being added to the users table"""

        with app.test_client() as client:
            new_user = {'f_name':'Colt', 'l_name':'Steele', 'i_url':''}
            resp = client.post('/users/new', data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Steele', html)
            self.assertIn('Add User', html)

    def test_details_page(self):
        """Post a new user, then test for said user in /details page"""

        with app.test_client() as client:
            new_user = {'f_name':'Aaron', 'l_name':'Brant', 'i_url':''}
            client.post('/users/new', data=new_user, follow_redirects=True)

            user = User.query.filter_by(first_name = 'Aaron').first()
            resp = client.get(f'/users/{user.id}')        
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Brant', html)
            self.assertIn('class="img-thumbnail" alt="user image">', html)

    def test_delete_user(self):
        """Post a new user, then delete said user"""

        with app.test_client() as client:
            new_user = {'f_name':'Naomi', 'l_name':'Issuper', 'i_url':''}
            client.post('/users/new', data=new_user)

            user = User.query.filter_by(first_name = 'Naomi').first()
            resp = client.post(f'/users/{user.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Naomi Issuper', html)
            self.assertIn('<form class="mt-2" action="/users/new">', html)
            