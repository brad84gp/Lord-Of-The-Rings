from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, UserCharacters
from logic import headers, get_books, get_chapters, get_movies, get_all_characters, add_fav_char, get_single_character
from Form import RegisterForm, LoginForm
import requests



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lotr_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'thisIStheKEY'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)



@app.route('/', methods=['GET', 'POST'])
def base_page():
    if session.get('user_id'):
        session.pop('user_id')

    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data

        new_user = User.create_user(first_name, last_name, username, password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Welcome To The Fellowship!')
        return redirect(f'/Home/{new_user.id}')
    
    form2 = LoginForm()
    if form2.validate_on_submit():
        username = form.username.data
        password = form.password.data

        login_user = User.authenticate_user(username, password)

        if login_user:
            session['user_id'] = login_user.id
            return redirect(f"/Home/{login_user.id}")
        else:
            form2.username.errors = ['Invalid username/password']
    
    return render_template('base.html', form=form, form2=form2)

@app.route('/LOTR-books')
def list_all_books():
    if session.get('user_id'):
        userid = session.get('user_id')
        user = User.query.get(userid)
    

        response = get_books()

        data = response.json()

        book_titles_chapters = []
        book_chapters = []
        book_info = {}
        
        for x in data['docs']:
            name = x['name']
            chapters = get_chapters(x['_id'])
            chapter_data = chapters.json()
            book_chapters = []
            for chapter in chapter_data['docs']:
                book_chapters.append(chapter['chapterName'])
                update = {name: book_chapters}
            book_info.update(update)

        return render_template('books.html', books=book_info, user=user)
    else:
        response = get_books()

        data = response.json()

        book_titles_chapters = []
        book_chapters = []
        book_info = {}
        
        for x in data['docs']:
            name = x['name']
            chapters = get_chapters(x['_id'])
            chapter_data = chapters.json()
            book_chapters = []
            for chapter in chapter_data['docs']:
                book_chapters.append(chapter['chapterName'])
                update = {name: book_chapters}
            book_info.update(update)

        return render_template('books.html', books=book_info)
            

    

@app.route('/LOTR-characters')
def get_characters():
    id = session.get('user_id')

    if session.get('user_id'):
        userid = session.get('user_id')
        user = User.query.get(userid)

        characters = get_all_characters()

        return render_template('characters.html', user=user, characters=characters)
    else:
        user = User.query.get(id)
        characters = get_all_characters()

        return render_template('characters.html', user=user, characters=characters)


@app.route('/LOTR-movies')
def get_movies():
    userid = session.get('user_id')
    user = User.query.get(userid)
    
    response = requests.get('https://the-one-api.dev/v2/movie', headers=headers)

    data = response.json()

    movie_ids = []

    for x in data['docs']:
        movie_ids.append(x['_id'])

    movie_info = []


    for x in movie_ids:
        response = requests.get(f'https://the-one-api.dev/v2/movie/{x}', headers=headers)

        data = response.json()

        for info in data['docs']:
            movie_data = {
                "Movie Title": info['name'],
                "Run Time": info['runtimeInMinutes'],
                "Budget In Millions": info['budgetInMillions'],
                "Box Office Revenu In Millions": info['boxOfficeRevenueInMillions'],
                "Academy Award Nominatations": info['academyAwardNominations'],
                "Academ Award Wins": info['academyAwardWins'],
                "Rotten Tomates Score": info['rottenTomatesScore']
            }
            movie_info.append(movie_data)

    return render_template('movies.html', user=user, movies=movie_info, movie_id=movie_ids)
    



@app.route('/Home/<int:user_id>')
def user_home_page(user_id):
    user = User.query.get(user_id)
    characters = UserCharacters.query.filter_by(userid=user_id).all()


    return render_template('userHome.html', user=user, characters=characters)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    return redirect("/")


@app.route('/editProfile/<int:user_id>')
def edit_profile(user_id):
    user = User.query.get(user_id)

    return render_template('updateProfile.html', user=user)


@app.route('/editProfile/<int:user_id>', methods=['POST'])
def edit_profile_success(user_id):
    user = User.query.get(user_id)

    firstname = request.form['first_name']
    lastname = request.form['last_name']
    username = request.form['username']
    image = request.form['image']
    bio = request.form['bio']

    returnValue = User.update_information(user.id, firstname, lastname, username, bio, image)

    if returnValue:
        flash('Change Successful')
        return render_template('updateProfile.html', user=user)
    else:
        flash('Something went wrong, please try again')
        return render_template('updateProfile.html', user=user)



@app.route('/changePassword/<int:user_id>')
def change_password(user_id):
    user = User.query.get(user_id)

    return render_template('updatePassword.html', user=user)


@app.route('/changePassword/<int:user_id>', methods=['POST'])
def password_change_success(user_id):
    user = User.query.get(user_id)

    old_password = request.form['password']
    new_password1 = request.form['newpassword']
    new_password2 = request.form['secondpassword']
    
    existing_user = User.authenticate_user(user.username, old_password)

    password = new_password1 if new_password1 == new_password2 else None
    if password == None or existing_user == False:
        flash('Either old password is incorrect or new passwords do not match')

        return render_template('updatePassword.html', user=user)
    else:
        password = User.encrypt_password(password)
        user.password = password
        db.session.commit()

        flash('Change successful')
        return redirect(f'/editProfile/{user.id}')


@app.route('/favMe/<int:user_id>/<name>')
def add_favorite_character(user_id, name):
    user = User.query.get(user_id)
    response = add_fav_char(name)

    for x in response['docs']:

        character_id = x['_id']
        name = x['name']
        height = x['height'] 
        race = x['race']
        gender = x['gender']
        birth = x['birth']
        spouse = x['spouse']
        death = x['death']
        realm = x['realm']
        hair = x['hair']
        wikiLink = x['wikiUrl']

        new_fav_char = UserCharacters(character_id=character_id, name=name, height=height, race=race, gender=gender,
        birth=birth, spouse=spouse, death=death, realm=realm, hair=hair, wikiLink=wikiLink)
        user.characters.append(new_fav_char)
        db.session.commit()

    return redirect(f'/Home/{user.id}')

    