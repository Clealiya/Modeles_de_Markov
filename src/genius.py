import os
from typing import Dict, Union, Tuple, List, Optional
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from sklearn.manifold import MDS

from icecream import ic

from data import get_genius_data
from ngram import ngram
from perplexite import perplexite


ARTISTS_LIST = ['JUL', 'Ninho', 'OrelSan', 'PNL', 'Lomepal', 'Damso', 'Nekfeu', 'Stromae', 'Gazo', 'Angèle']


# les keys des dictionnaires soint soit des str pour le unigram, Tuple[str, str] pour le bigrame 
# set Tuple[str, str, str] pour le trigame
key_type = Union[str, Tuple[str, str], Tuple[str, str, str]]
dico_type = Dict[key_type, int]


def perplexite_between_artist(artist: str, 
                              dico_list: List[List[dico_type]], 
                              vocabs_list: List[int]) -> np.ndarray:
    """ calcule la perplexité des artistes sur un artite en particulier """
    output = []         # ouput[i][j] -> perplexité du (j+1)-gram de l'artist i par 
                        #                rapport au texte test de <artist>
    test_file = get_genius_data(mode='test', artist=artist)
    for i in range(len(dico_list)):
        perplex_i = []
        for n in range(3):
            perplex_i.append(perplexite(dico_list[i][n], 
                                        text=test_file, 
                                        n=n + 1, 
                                        V=vocabs_list[i], 
                                        dico_n_1_gram=dico_list[i][n - 1] if n > 0 else None))
        output.append(perplex_i)
    return np.array(output)
    


def compare_artists(artists_name: List[str],
                    plot: Optional[bool]=True,
                    process_MDS: Optional[bool]=False) -> None:
    """ compare les ngrams des artistes entre eux """
    result_path = os.path.join('..', 'results', 'genius_results')
    dico_list = []      # dico_list[i][j] -> (j+1)-gram de l'artiste i
    vocabs_list = []    # dico_size[i] -> taille du vocabulaire de l'artiste i

    for i in range(len(artists_name)):
        train_file = get_genius_data(mode='train', artist=artists_name[i])
        dicos = []
        for n in range(1, 4):
            dicos.append(ngram(text=train_file, n=n))
        vocabs_list.append(len(dicos[0]))
        dico_list.append(dicos)
        del dicos
    
    all_p = []

    if plot:
        plot_vocab_size(artists_name, vocabs_list, result_path)

    for artist in tqdm(artists_name):
        p = perplexite_between_artist(artist, dico_list, vocabs_list)
        all_p.append(p)
        if plot:
            for n in range(1, 4):
                plot_perplexite_between_artist(artist, artists_name, perplexite=p, n=n, result_path=result_path)
    
    if process_MDS:
        for i in range(1, 4):
            run_MDS(all_p=np.array(all_p), artists_name=artists_name, n_gram=i, result_path=result_path)



def plot_vocab_size(artists_name: List[str], 
                    vocabs_list: List[int], 
                    result_path: str) -> None:
    """ affiche la tailles du vocabulaire pour chacun des artistes"""
    plt.figure(figsize=(10, 6))
    plt.bar(artists_name, vocabs_list)

    plt.xlabel('Artistes')
    plt.ylabel('Nombre de mots unique')
    plt.title('Nombre de mots unique par artiste')
    # plt.xticks(rotation=45, ha='right')

    plt.tight_layout()  
    plt.savefig(os.path.join(result_path, 'vocab_size_per_artist.png'))


def plot_perplexite_between_artist(artist: str, 
                                   artists_name: List[str], 
                                   perplexite: np.ndarray, 
                                   n: int, 
                                   result_path: str) -> None:
    """ affiche la perplexité des artistes par rapport un un artiste en particulier """
    plt.figure(figsize=(10, 6))
    p = perplexite[:, n - 1]
    indices_tries = np.argsort(p)[::-1]
    artists_name_tries = [artists_name[i] for i in indices_tries]

    plt.bar(artists_name_tries, p[indices_tries])

    plt.xlabel('Artistes')
    plt.ylabel('perplexité')
    plt.title('Perplxité suivant un corpus de ' + artist)
    # plt.xticks(rotation=45, ha='right')

    plt.tight_layout()  
    figname = artist + '_' + str(n) + '.png'
    plt.savefig(os.path.join(result_path, figname))
    plt.close()
    

def run_MDS(all_p: np.ndarray,
            artists_name: List[str],
            n_gram: int,
            result_path: str) -> None:
    n = len(artists_name)

    # Calcule la distance
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i, j] = (all_p[i, j, n_gram - 1] + all_p[j, i, n_gram - 1]) / 2
    
    # fait la MDS
    mds = MDS(n_components=2, dissimilarity="precomputed")
    coordinates_2d = mds.fit_transform(distances)

    # Plot
    plt.figure(figsize=(8, 6))
    for (x, y), label in zip(coordinates_2d, artists_name):
        plt.scatter(x, y, label=label)
    for (x, y), label in zip(coordinates_2d, artists_name):
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center')

    # plt.legend()
    plt.grid(True)
    plt.title('Projection en 2D des artistes')

    plt.savefig(os.path.join(result_path, f"MDS_{n_gram}.png"))
    # plt.savefig(os.path.join(result_path, f"MDS_{n_gram}.svg"))



if __name__ == '__main__':
    compare_artists(ARTISTS_LIST,
                    plot=False,
                    process_MDS=True)
