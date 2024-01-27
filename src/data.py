# -*- coding: utf-8 -*-
import os
from typing import Callable, List, Union, Optional



def getfile_dumas(mode: Optional[str] = None, 
                  mask: Optional[bool] = None) -> List[str]:
    """
    permet de récuperer le chemin des fichiers de données.
    vous pouvez indiquer:
        - mode: train, test ou None (si vous voulez les données entières)
        - mask: None ou True
    
    retourne une liste de chemin vers les fichiers spécifier
    """
    TEXT = ['La_Reine_Margot',
            'Le_comte_de_Monte_Cristo',
            'Le_Vicomte_de_Bragelonne',
            'Les_Trois_Mousquetaires',
            'Vingt_ans_apres']
    PATH = os.path.join('..', 'data', 'alexandre_dumas')

    data = []
    for text in TEXT:
        file = os.path.join(PATH, text)
        if mode is not None:
            file += '.' + mode + '.tok'
        else:
            file += '.tok'
        if mask is not None:
            for i in range(1, 4):
                data.append(file + '.100.' + str(i) + '.mask')
        else:
            data.append(file)

    verifpath(data)
    return data


def verifpath(data: List[str]) -> None:
    """
    affiche des messages d'erreur dans le cas où un chemin n'existe pas
    """
    for d in data:
        if not os.path.isfile(d):
            print("Attention probleme de generation du fichier:", d)


def openfile(file: str, line_by_line: Optional[bool]=False) -> Union[List[str], List[List[str]]]:
    """
    prend un chemin ou une liste de chemain vers un texte 
    et renvoie la liste de mots que contients ce texte
    si line_bu_line = True, renvoie la liste de phrase (donc une list de list de mots)
    """
    text = []

    with open(file, 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.split(' ')
            if line[-1] == '\n':
                line = line[:-1]
            if line[0] == '<s>':
                line = line[1:]
            if line[0] == '<s>':
                line = line[1:]
            
            if not(line_by_line):
                text += line
            else:
                text.append(line)
    
    return text


def save_dico(dico1: dict, 
              dico2: dict, 
              dico3: dict, 
              folder: str, 
              file: str, 
              sorting: Optional[Callable[[str], int]] = None) -> None:
    """
    Enregistre les dictionnaires des {1, 2, 3}-grams dans le fichier texte: <folder>/<file>
    on peut aussi trier les dictonnaires avec sorting. exemple: sorting=lambda x:x[1] trira les dictionnaires en fonction de leurs valeurs
    """
    path = os.path.join(folder, file)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if sorting is not None:
        dico1 = dict(sorted(dico1.items(), key=sorting, reverse=True))
        dico2 = dict(sorted(dico2.items(), key=sorting, reverse=True))
        dico3 = dict(sorted(dico3.items(), key=sorting, reverse=True))

    with open(path, 'w', encoding='utf8') as f:
        f.write('#unigrams {}\n'.format(len(dico1)))
        for key, value in dico1.items():
            f.write(str(key) + ' : ' + str(value) + '\n')
        
        f.write('#bigrams {}\n'.format(len(dico2)))
        for key, value in dico2.items():
            f.write(str(key) + ' : ' + str(value) + '\n')

        f.write('#trigrams {}\n'.format(len(dico3)))
        for key, value in dico3.items():
            f.write(str(key) + ' : ' + str(value) + '\n')
    
    f.close()
    print('fichier enregistré dans', path)


def get_balzac_data(mode: str) -> List[str]:
    assert mode in ['train', 'test'], "mode must be train or test"
    balzac_path = os.path.join('..', 'data', 'balzac_tokenized')
    file = mode + '.txt'
    output = openfile(file=os.path.join(balzac_path, file))
    return output


def get_genius_data(mode: str, artist: str) -> List[str]:
    assert mode in ['train', 'test'], "mode must be train or test"

    artist_list = []
    with open(file=os.path.join('..', 'genius', 'artists.txt'), mode='r', encoding='utf8') as f:
        for line in f.readlines():
            artist_list.append(line[:-1])
        f.close()
    assert artist in artist_list, "artist must be in " + str(artist_list)

    file = os.path.join('..', 'data', 'genius_lyrics_tokenized', artist + '_' + mode + '.txt')
    output = openfile(file=file)
    return output



if __name__ == '__main__':
    # data = getfile_dumas(mode='train')
    # print(data)
    print(get_genius_data(mode='train', artist='Angèle'))