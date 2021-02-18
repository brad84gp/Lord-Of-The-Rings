import requests
from config import headers




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
   
def add_fav_char(name):
    response = requests.get(f'https://the-one-api.dev/v2/character?name={name}', headers=headers)
    data = response.json()

    return data

def get_single_character(name):
    response = requests.get(f'https://the-one-api.dev/v2/character?name={name}', headers=headers)
    data = response.json()

    characters_list = []

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
        characters_list.append(character_info)

    return characters_list