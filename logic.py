import requests
from config import headers
from models import db, connect_db, User, UserCharacters, UserMovies, UserPosts




def get_books():
    response = requests.get('https://the-one-api.dev/v2/book')
    return response

def get_chapters(id):
    chapters = requests.get(f'https://the-one-api.dev/v2/chapter?book={id}', headers=headers)
    return chapters


def get_all_characters():
    response = requests.get('https://the-one-api.dev/v2/character', headers=headers)
    data = response.json()
    
   
    characters = []

    
    for x in data['docs']:
        try:
            if x['wikiUrl']:
                    wikiUrl = x['wikiUrl']
        except:
            wikiUrl = ""

        character_info = {
            "Name": x['name'],
            "Height": x['height'],
            "Race": x['race'],
            "Birth": x['birth'],
            "Spouse": x['spouse'],
            "Death": x['death'],
            "Realm": x['realm'],
            "Hair": x['hair'],
            "WikiLink": wikiUrl
        }
        characters.append(character_info)

    return characters

def get_movies():
    

    return movie_info
   
def add_fav_char(user_id, name):
    user = User.query.get(user_id)
    response = requests.get(f'https://the-one-api.dev/v2/character?name={name}', headers=headers)
    data = response.json()

    for x in data['docs']:

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


# def get_single_character(name):
#     response = requests.get(f'https://the-one-api.dev/v2/character?name={name}', headers=headers)
#     data = response.json()

#     characters_list = []

#     for x in data['docs']:
#         try:
#             if x['wikiUrl']:
#                     wikiUrl = x['wikiUrl']
#         except:
#             wikiUrl = ""

#         character_info = {
#             "Name": x['name'],
#             "Height": x['height'],
#             "Race": x['race'],
#             "Birth": x['birth'],
#             "Spouse": x['spouse'],
#             "Death": x['death'],
#             "Realm": x['realm'],
#             "Hair": x['hair'],
#             "WikiLink": wikiUrl
#         }
#         characters_list.append(character_info)

#     return characters_list


def add_fav_movie(user_id, name):
    user = User.query.get(user_id)
    response = requests.get(f'https://the-one-api.dev/v2/movie?name={name}', headers=headers)
    data = response.json()

    for x in data['docs']:

        movie_id = x['_id'],
        name = x['name'],
        runtime = x['runtimeInMinutes'],
        budget = x['budgetInMillions'],
        boxoffice = x['boxOfficeRevenueInMillions'],
        academy_nominations = x['academyAwardNominations'],
        academy_wins = x['academyAwardWins'],
        rotten_score = x['rottenTomatesScore']

        new_fav_movie = UserMovies(movie_id=movie_id, name=name, runtime=runtime, budget=budget, boxoffice=boxoffice,
        academy_nominations=academy_nominations, academy_wins=academy_wins, rotten_score=rotten_score)
        user.movies.append(new_fav_movie)
        db.session.commit()
  

def search_for_character(name):
    print(name)
    name = name.title()
    print(name)
    response = requests.get(f'https://the-one-api.dev/v2/character?name={name}', headers=headers)
    data = response.json()
    print(data)

    if data['docs']:

        for x in data['docs']:
            char_id = x['_id']
        response2 = requests.get(f'https://the-one-api.dev/v2/character/{char_id}/quote', headers=headers)
        data2 = response2.json()

        character_info = []
        
        if data2['docs']:
            for x in data2['docs']:
                info = {
                    'Dialog' : x['dialog']
                }
                character_info.append(info)
            
            return character_info
        else:
            return 'no quote found'
    else:
        return False
