import lyricsgenius as gen
import os
import shutil
from typing import List


DATA_PATH = os.path.join('..', 'data', 'genius_lyrics')


def get_token() -> str:
    with open('API_token.txt') as f:
        for line in f:
            return line
        

def add_underscore(string: str) -> str:
    """ remplace les caractère probématique par un underscore """
    special_caractere = [' ', "'", '"', '-']
    new_string = ''
    for c in string:
        if c in special_caractere:
            new_string += '_'
        else:
            new_string += c
    return new_string
        

def save_songs(artiste: str, nb_song: int, path: str) -> None:
    """ sauvegarde les paroles des <nb_song> musiques les plus populaires de <artiste>"""
    output = genius.search_artist(artiste, max_songs=nb_song, sort='popularity')
    songs = output.songs
    artist_path = os.path.join(path, artiste)
    for song in songs:
        song_dict = song.to_dict()
        title = song_dict['title']
        filename = artiste + '_' + add_underscore(title) + '.txt'

        # Si le dossier n'existe pas, on le crée
        if not os.path.exists(artist_path):
            os.makedirs(artist_path)
        
        # On sauvegarde la musique seulement si est n'y est pas déjà
        if not(filename in os.listdir(artist_path)):
            song.save_lyrics(filename=filename, extension='txt')
            try:
                shutil.move(filename, artist_path)
            except:
                print('attention', filename, "n'a pas été déplacé!")



def read_artists_file(filepath: str) -> List[str]:
    """ Renvoie la liste des artises dans un fichier txt spécifier """
    artists = []
    with open(filepath, 'r', encoding='utf8') as f:
        for line in f.readlines():
            artists.append(line[:-1] if line[-1] == '\n' else line)
    return artists
            

def get_data(artists: List[str], nb_song: int, path: str) -> None:
    """ sauvegarde les paroles des <nb_song> musiques les plus populaires des <artistes>"""
    for artist in artists:
        artist_path = os.path.join(path, artist)
        if os.path.exists(artist_path) and nb_song == len(os.listdir(artist_path)):
            print('musiques de', artist, 'deja sauvegardées')
        else: 
            print(artist)
            save_songs(artiste=artist, nb_song=nb_song, path=path)


if __name__ == "__main__":
    token = get_token()
    genius = gen.Genius(token)
    artists = read_artists_file('artists.txt')
    get_data(artists, nb_song=50, path=DATA_PATH)
