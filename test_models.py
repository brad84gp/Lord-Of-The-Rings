from unittest import TestCase

from app import app
from models import db, User, UserCharacters, UserMovies, UserPosts



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lotr_db_tes'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserTextCase(TestCase):

    def setup(self):
        User.query.delete()

    def tearDown(self):

        db.session.rollback()
    
    def test_create_user(self):

        user = User(first_name='bob', last_name='baggins', username='baggins85', password='baggins85bob')
        db.session.add(user)
        db.session.commit()

        user2 = User.query.filter_by(first_name=user.first_name).first()
        self.assertEquals(user, user2)
    
    def update_user(self):

        user = User(first_name='bob', last_name='baggins', username='baggins85', password='baggins85bob')
        user1 = user

        db.session.add(user)
        db.session.commit()

        user.first_name = billy
        user.last_name = joel
        user.username = billyjoelrocks
        user.password = rocksjoelbilly
        db.session.commit()

        user = User.query.get(1)

        self.assertNotEqual(user1, user)

        