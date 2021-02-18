from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)
    
    last_name = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False, unique=True)
    
    bio = db.Column(db.String, nullable=True)
    
    image = db.Column(db.Text, nullable=True, default='https://thednetworks.com/wp-content/uploads/2012/01/picture_not_available_400-300.png')


    
    def create_user(first_name, last_name, username, password):
        
        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode('utf8')

        return User(first_name=first_name, last_name=last_name, username=username, password=hashed_utf8)


    def encrypt_password(pwd):

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode('utf8')

        return hashed_utf8

    
    def update_information(userid, firstname, lastname, username, bio, image):
        user = User.query.get(userid)

        try: 
            if firstname != "":
                user.first_name = firstname
                db.session.commit()
            if lastname != "":
                user.last_name = lastname
                db.session.commit()
            if username != "":
                user.username = username
                db.session.commit()
            if bio != "":
                user.bio = bio
                db.session.commit()
            if image != "":
                user.image = image
                db.session.commit()

            return True
        except incorrectValueError:
            return False

        


    @classmethod
    def authenticate_user(cls, username, pwd):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
    
    

class UserCharacters(db.Model):

    __tablename__ = 'characters'

    

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    character_id = db.Column(db.Text, nullable=False)

    name = db.Column(db.Text, nullable=False)

    height = db.Column(db.Text, nullable=False)

    race = db.Column(db.Text, nullable=False)

    gender = db.Column(db.Text, nullable=False)

    birth = db.Column(db.Text, nullable=False)

    spouse = db.Column(db.Text, nullable=False)

    death = db.Column(db.Text, nullable=False)

    realm = db.Column(db.Text, nullable=False)

    hair = db.Column(db.Text, nullable=False)

    wikiLink = db.Column(db.Text, nullable=False)

    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', backref=db.backref('characters', cascade="all, delete-orphan"))


class UserMovies(db.Model):

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    movie_id = db.Column(db.Text, nullable=False)

    name = db.Column(db.Text, nullable=False)

    runtime = db.Column(db.Integer, nullable=False)

    budget = db.Column(db.Integer, nullable=False)

    boxoffice = db.Column(db.Integer, nullable=False)

    academy_nominations = db.Column(db.Integer, nullable=False)

    academy_wins = db.Column(db.Integer, nullable=False)

    rotten_score = db.Column(db.Integer, nullable=False)

    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', backref=db.backref('movies', cascade="all, delete-orphan"))

class UserPosts(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    post = db.Column(db.Text, nullable=False)

    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', backref=db.backref('posts', cascade="all, delete-orphan"))