from unittest import TestCase

from app import app
from models import db, connect_db, User, UserCharacters, UserMovies, UserPosts

connect_db(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lotr_db_tes'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserTestCase(TestCase):

    def setUp(self):

        User.query.delete()

        user = User(first_name='bob', last_name='baggins', username='baggins85', password='baggins85bob')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):

        db.session.rollback()

    def test_sign_up(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('user', html)

    def test_get_books(self):
        with app.test_client() as client:
            resp = client.get('/LOTR-books')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('books', html)

    def test_get_characters(self):
        with app.test_client() as client:
            resp = client.get('/LOTR-characters')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('characters', html)

    def test_get_movies(self):
        with app.test_client() as client:
            resp = client.get('/LOTR-movies')
            html = resp.get_data(as_text=True)
            

            self.assertEqual(resp.status_code, 200)
            self.assertIn('movies', html)

    def test_user_home(self):
        with app.test_client() as client:
            resp = client.get((f'/Home/{self.user_id}'), follow_redirects=True)
            html = resp.get_data(as_text=True)
            follow_redirects=True

            self.assertEqual(resp.status_code, 200)
            
    