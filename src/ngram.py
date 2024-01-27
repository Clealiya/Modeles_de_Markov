import os
from typing import List, Dict, Tuple, Union

from data import getfile_dumas, openfile, save_dico


# les keys des dictionnaires soint soit des str pour le unigram, Tuple[str, str] pour le bigrame 
# set Tuple[str, str, str] pour le trigame
key_type = Union[str, Tuple[str, str], Tuple[str, str, str]]
dico_type = Dict[key_type, int]


def unigram(text: List[str], have_vocab_size: bool) -> Tuple[dico_type, int]:
    """
    fait un 1-gram sur une liste de mots. Renvoie 
    - un dictionnaire contenant l'ensemble des mot vu avec leur nombre d'occurences 
    - le nombre de mots du vocabulaire
    """
    dico = {}
    for word in text:
        if word not in dico:
            dico[word] = 1
        else:
            dico[word] += 1

    if have_vocab_size:
         return dico, len(dico)
    
    return dico


def bigram(text: List[str], have_vocab_size: bool) -> Tuple[dico_type, int]:
    """
    fait un 2-gram sur une liste de mots. Renvoie:
    - un dictionnaire contenant l'ensemble des sequences de 2 mots vu avec leur nombre d'occurences
    - le nombre de mots du vocabaulaire
    """
    dico = {}
    V = []
    sequence = ('<s>', '<s>')
    for word in text:
            sequence = (sequence[1], word)
            if sequence not in dico:
                dico[sequence] = 1
            else:
                dico[sequence] += 1
            
            if have_vocab_size and word not in V:
                 V.append(word)
    
    if have_vocab_size:
         return dico, len(V)
    
    return dico


def trigram(text: List[str], have_vocab_size: bool) -> Tuple[dico_type, int]:
    """
    fait un 3-gram sur une liste de mots. Renvoie un dictionnaire contenant 
    l'ensemble des sequences de 3 mots vu avec leur nombre d'occurences
    """
    dico = {}
    V = []
    sequence = ('<s>', '<s>', '<s>')
    for word in text:
            sequence = (sequence[1], sequence[2], word)
            if sequence not in dico:
                dico[sequence] = 1
            else:
                dico[sequence] += 1

            if have_vocab_size and word not in V:
                 V.append(word)

    if have_vocab_size:
         return dico, len(V)
    
    return dico


def ngram(text: List[str], n: int, have_vocab_size: bool=False) -> Tuple[dico_type, int]:
        assert 1 <= n <= 3, "n doit être un entier entre 1 et 3"
        
        if n == 1:
             return unigram(text, have_vocab_size)
        elif n == 2:
             return bigram(text, have_vocab_size)
        return trigram(text, have_vocab_size)


if __name__ == '__main__':
    files = getfile_dumas()
    for file in files:
        print('file:', file)
        words = openfile(file)
        dico1, V = ngram(words, 1, have_vocab_size=True)
        dico2, dico3 = ngram(words, 2), ngram(words, 3)
        save_dico(dico1, dico2, dico3,
                os.path.join('..', 'results', 'ngram'),
                file.split('\\')[2] + '.txt',
                sorting=lambda x:x[1])
        print(f'vocab size: {V}')
