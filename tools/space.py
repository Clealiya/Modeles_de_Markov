"""
parfois dans les données, on a pas d'espace entre <s> et le premier mot. Le but de ce programme
est de modifier les données de tel sorte qu'il rajoute des espaces entre <s> mot
"""
import os
from tqdm import tqdm


def add_space(file: str) -> None:
    data = []
    with open(file, mode='r', encoding='utf8') as f:
        for line in f.readlines():
            data.append(line)
        f.close()
    
    index_space = 7 
    new_data = []
    for i in tqdm(range(len(data)), desc='copy and remove space'):
        if len(data[i]) > index_space and data[i][index_space] == ' ':
            new_data.append(data[i])
        else:
            new_data.append(data[i][:index_space] + ' ' + data[i][index_space:])
    del data

    with open(file, mode='w', encoding='utf8') as f:
        for line in new_data:
            f.write(line)
        f.close()



if __name__ == '__main__':
    # data_path = os.path.join('..', 'data', 'balzac_tokenized')
    # add_space(os.path.join(data_path, 'train.txt'))
    # add_space(os.path.join(data_path, 'test.txt'))

    genius_path = os.path.join('..', 'data', 'genius_lyrics_tokenized')
    for artist in os.listdir(os.path.join('..', 'data', 'genius_lyrics')):
        add_space(os.path.join(genius_path, artist + '_train.txt'))
        add_space(os.path.join(genius_path, artist + '_test.txt'))