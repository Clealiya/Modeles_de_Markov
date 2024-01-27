import os


def merge_txt(path, split, train_file, test_file):

    fichiers = [f for f in os.listdir(path) if f.endswith('.txt')]
    n = len(fichiers)

    fichiers_train = fichiers[:int(split * n)]
    fichier_test = fichiers[int(split * n):]

    with open(train_file, 'w', encoding='utf8') as fichier_train:
        for fichier in fichiers_train:
            chemin_complet = os.path.join(path, fichier)
            with open(chemin_complet, 'r') as f:
                contenu = f.read()
                fichier_train.write(contenu)
    
    with open(test_file, 'w', encoding='utf8') as fichier_train:
        for fichier in fichier_test:
            chemin_complet = os.path.join(path, fichier)
            with open(chemin_complet, 'r') as f:
                contenu = f.read()
                fichier_train.write(contenu)


if __name__ == "__main__":
    # path = os.path.join('..', 'data', 'balzac_tokenized')
    # merge_txt(path, 
    #           split=0.8, 
    #           train_file=os.path.join(path, 'train.txt'),
    #           test_file=os.path.join(path, 'test.txt'))

    # path = os.path.join('..', 'data', 'genius_lyrics_tokenized')
    # for artist in os.listdir(path):
    #     artist_path = os.path.join(path, artist)
    #     merge_txt(artist_path, 
    #               split=0.8,
    #               train_file=os.path.join(path, artist + '_train.txt'),
    #               test_file=os.path.join(path, artist + '_test.txt'))
    pass