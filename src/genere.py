from typing import List

from data import getfile_dumas, openfile
from ngram import ngram
from devine import devine


def genere(file_train: str, n_gram: int, nb_mot_max: int, input: List[str]=[]) -> List[str]:
    text = openfile(file_train)
    dico = ngram(text, n_gram)
    del text

    text = ['<s>' for _ in range(n_gram)] + input
    while text[-1] != '</s>' and len(text) < nb_mot_max:
        sequence = tuple(text[-(n_gram - 1):]) if n_gram > 1 else ()
        predict = devine(sequence, dico)
        text.append(predict)

    return text[n_gram:]


def merge(text: List[str]) -> str:
    """ converte a list of str into a str with space btw word"""
    string = ''
    for word in text:
        string += word + ' '
    return string


if __name__ == '__main__':
    input = [[], ['il'], ['il', 'prononçait']]
    file = getfile_dumas(mode='train')[0]
    for n in range(1, 4):
        text_predict = genere(file, n_gram=n, nb_mot_max=50, input=input[n-1])
        text_predict = merge(text_predict)
        print(f"n:{n} -> {text_predict}")
    