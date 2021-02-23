from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, UserCharacters, UserMovies, UserPosts, API_KEY
from logic import headers, get_books, get_chapters, get_movies, get_all_characters, add_fav_char, add_fav_movie, search_for_character
from Form import RegisterForm, LoginForm
import requests
import os
import psycopg2


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get
    ('DATABASE_URL', 'postgresql:///lotr_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config["SECRET_KEY: str"] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'thisIStheKEY')
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

    user = User.query.get(id)
    characters = get_all_characters()

    return render_template('characters.html', user=user, characters=characters)

@app.route('/search', methods=['POST'])
def search_character():
    id = session.get('user_id')

    user = User.query.get(id)

    name = request.form['searchBox']

    character_info = search_for_character(name)
    
    if character_info:
        return render_template('searchedCharacter.html', user=user, character=character_info)
    elif character_info == 'no quote found':
        flash(f'No quotes were found for {name}')
        return redirect('/LOTR-characters')
    else:
        flash('Name did not exist OR it was typed wrong. Try again and be sure to Capitalize first and last names!')
        return redirect('/LOTR-characters')




@app.route('/LOTR-movies')
def get_movies():
    if session.get('user_id'):
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

        return render_template('movies.html', user=user, movies=movie_info)
    else:
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

        return render_template('movies.html', movies=movie_info)

    



@app.route('/Home/<int:user_id>')
def user_home_page(user_id):
    if session.get('user_id'):
        user = User.query.get(user_id)
        characters = UserCharacters.query.filter_by(userid=user_id).all()
        movies = UserMovies.query.filter_by(userid=user_id).all()
        posts = UserPosts.query.filter_by(userid=user_id).all()

        return render_template('userHome.html', user=user, characters=characters, movies=movies, posts=posts)
    else:
        flash('Login Required!')
        return redirect("/")

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




"""

    - This is where the routes are that handle the adding and removing of 
        characters, movies and posts to their home page

    - The logic has been seperated into a seperate file for cleaner more readable
        code within the logig.py file

"""


@app.route('/favMe/<int:user_id>/<name>/<fav_type>')
def add_favorite_character(user_id, name, fav_type):
    user = User.query.get(user_id)

    if fav_type == 'character':
        characters = UserCharacters.query.filter_by(userid=user_id).all()

        if len(characters) <= 2:
            
            add_fav_char(user_id, name)

            return redirect(f'/Home/{user.id}')
        else:
            flash('Already have 3 favorite characters, please remove one before you add another!')
            return redirect('/LOTR-characters')
    elif fav_type == 'movie':
        movies = UserMovies.query.filter_by(userid=user_id).all()

        if len(movies) <=2:

            add_fav_movie(user_id, name)

            return redirect(f'/Home/{user.id}')
        else:
            flash('Already have 3 favorite movies, please remove one before you add another!')
            return redirect('/LOTR-movies')


    

@app.route('/remove/<name>/<int:user_id>')
def remove_fav_character(name, user_id):
    user = User.query.get(user_id)
    characters = UserCharacters.query.filter_by(userid=user_id).all()

    movies = UserMovies.query.filter_by(userid=user_id).all()

    for character in characters:
        if character.name == name:
            db.session.delete(character)
            db.session.commit()
    for movie in movies:
        if movie.name == name:
            db.session.delete(movie)
            db.session.commit()

    return redirect(f'/Home/{user.id}')

@app.route('/addPost/<int:user_id>', methods=['POST'])
def add_post(user_id):
    user = User.query.get(user_id)

    title = request.form['title']
    post = request.form['post']
    
    if title == "" or post == "":
        flash('Please fill out both title and post')
        return redirect(f'/Home/{user.id}')
    else:
        new_post = UserPosts(title=title, post=post)

        user.posts.append(new_post)

        db.session.commit()

        return redirect(f'/Home/{user.id}')



   

@app.route('/removePost/<int:user_id>/<post_title>')
def remove_post(user_id, post_title):
    user = User.query.get(user_id)
    post_to_remove = UserPosts.query.filter_by(title=post_title).first()

    db.session.delete(post_to_remove)
    db.session.commit()

    return redirect(f'/Home/{user.id}')

@app.route('/mainFeed')
def get_all_posts():
    id = session.get("user_id")
    user = User.query.get(id)
    posts = UserPosts.query.all()

    return render_template('mainFeed.html', user=user, posts=posts)

@app.route('/deleteAccount/<int:user_id>')
def delete_account(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    flash('Account Deleted')
    return redirect('/')