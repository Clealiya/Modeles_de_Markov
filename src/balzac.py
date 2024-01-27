import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from typing import List

from data import get_balzac_data
from ngram import ngram
from perplexite import perplexite



def balzac(linspace: int) -> None:
    """ run ngram for n=1, 2 and 3 and save result in balzac_result"""
    train_data = get_balzac_data(mode='train')
    test_data = get_balzac_data(mode='test')

    data_rates = np.linspace(0, 1, linspace + 1)[1:]
    lines = data_rates * len(train_data)
    lines = lines.astype(int)
    perplexite_list = [[], [], []]
    vocab_size_list = []


    for end_line in tqdm(lines):
        dico1, V = ngram(train_data[:end_line], 1, have_vocab_size=True)
        dico2 = ngram(train_data[:end_line], 2, have_vocab_size=False)
        dico3 = ngram(train_data[:end_line], 3, have_vocab_size=False)
        
        perplex1 = perplexite(dico1, test_data, n=1, V=V, dico_n_1_gram=None)
        perplex2 = perplexite(dico2, test_data, n=2, V=V, dico_n_1_gram=dico1)
        perplex3 = perplexite(dico3, test_data, n=3, V=V, dico_n_1_gram=dico2)

        perplexite_list[0].append(perplex1)
        perplexite_list[1].append(perplex2)
        perplexite_list[2].append(perplex3)
        vocab_size_list.append(V)
    

    path = os.path.join('results', 'balzac_result')
    for n in range(4):
        plot(lines, perplexite_list, path=path, mode='lines', n=n)

        plot(vocab_size_list, perplexite_list, path=path, mode='vocab_size', n=n)


def plot(x: List[float], y: List[List[float]], mode: str, path: str, n: int) -> None:
    assert mode in ['lines', 'vocab_size'], 'mode doit être lines ou vocab_size'

    if mode == 'lines':
        title = "Perplexité d'un n-gram en fonction du nombres de ligne d'un corpus"
        xlabel = "nombre de lignes d'un corpus"
        
    else:
        title = "Perplexité d'un n-gram en fonction de la taille du vocabulaire"
        xlabel = "taille du vocabaulaire"

    if n != 3:
        filename = f"balzac_{n+1}_{mode}"
        plt.plot(x, y[n])
    else:
        filename = f"balzac_all_{mode}"
        for i in range(3):
            plt.plot(x, y[i])
        plt.legend(['unigram', 'bigram', 'trigram'])
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Perplexité évalué sur corpus différant de l'entraînement")
    plt.savefig(os.path.join(path, filename + '.png'))  # png format
    # plt.savefig(os.path.join(path, filename + '.svg'))  # svg format
    plt.clf()



if __name__ == '__main__':
    balzac(linspace=100)
    