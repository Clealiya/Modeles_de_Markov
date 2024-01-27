from typing import Union, List, Dict, Tuple
from numpy import log, exp

from data import getfile_dumas, openfile
from ngram import ngram


# les keys des dictionnaires soint soit des str pour le unigram, Tuple[str, str] pour le bigrame 
# set Tuple[str, str, str] pour le trigame
key_type = Union[str, Tuple[str, str], Tuple[str, str, str]]
dico_type = Dict[key_type, int]


def perplexite(dico: dico_type, 
               text: List[str], 
               n: int,
               V: int, 
               dico_n_1_gram: dico_type=None) -> float:
    """
    Calcule la perplexité du texte avec le dictionnaire dico qui est le dicotaionre appris d'un
    texte d'entraînement d'un n-gram. V est la taille du vocabulaire
    """
    llp = 0                         # logarithme de la perplexité
    N_test = len(text)              # nombre de mots dans le text de test
    N_train = sum(dico.values())    # nombre de mots dans le texte de train

    sequence = init_sequence(n)
    for word in text:
        sequence = update_sequence(n, sequence, word)
        llp -= log_perplexite_with_LP(n, N_train, V, dico, sequence, dico_n_1_gram) / N_test

    return exp(llp) 


def run_perplexite(file_train: str, file_test: str, n: int) -> None:
    """
    Prend un corpus de train (file_train), entraîne un ngram desus (n),
    et calcule la perplexité du texte de test (file_test)
    Renvoie la perplexité
    """
    text_train = openfile(file_train)
    dico, V = ngram(text_train, n, have_vocab_size=True)
    dico_n_1_gram = ngram(text_train, n - 1) if n > 1 else None

    del text_train
    text_test = openfile(file_test)
    
    llp = perplexite(dico, text_test, n, V, dico_n_1_gram)
    return llp



def init_sequence(n: int) -> key_type:
    """
    Crée une séquence de <s> de taille n pour l'initialisation de la séquence
    """
    if n == 1:
        return '<s>'
    if n == 2:
        return ('<s>', '<s>')
    return ('<s>', '<s>', '<s>')


def update_sequence(n: int, sequence: key_type, new_word: str) -> key_type:
    """
    update la séquence avec un nouveau mots
    """
    if n == 1:
        return new_word
    if n == 2:
        return (sequence[1], new_word)
    return (sequence[1], sequence[2], new_word)


def log_perplexite_with_LP(n: int, 
                           N: int, 
                           V: int, 
                           dico: key_type, 
                           sequence: key_type, 
                           dico_n_1_gram: key_type) -> float:
    """
    Calcule le log(perplexité avec Laplace)
    """
    occ_seq = dico[sequence] if sequence in dico else 0
    
    if n == 1:
        lp = (occ_seq + 1) / (N + V) 
    else:
        occ_old_seq = dico_n_1_gram[sequence[:-1]] if sequence[:-1] in dico_n_1_gram else 0
        lp = (occ_seq + 1) / (occ_old_seq + V) 

    return log(lp)


if __name__ == "__main__":
    for i in range(5):
        file_train = getfile_dumas(mode='train')[i]
        file_test = getfile_dumas(mode='test')[i]
        print(f'{file_train = } \n{file_test = }')

        for n in range(1, 4):
            llp = run_perplexite(file_train, file_test, n=n)
            print('perplexité pour n =', n, '-> llp =', llp)
