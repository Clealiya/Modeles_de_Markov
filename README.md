Le projet consiste à programmer un modèle de langage markovien sous différentes 
modalités. À partir de ces modèles, nous allons en calculer les performances 
à l’aide de la métrique de la perplexité. Puis, nous allons implémenter
le remplissage de textes à trous et la génération de texte.

## Contenu

Dans ce projet vous trouverez les dossiers et fichiers suivants:

- `/data`: dossier contenant les données (textes d'Alenxandre Dumas, textes de Balzac, et des musiques de Genius) qui sont tokenisées.
- `/genius`: dossier contenant le script pour scraper les textes des chanteurs avec l'API de genius.
- `/rapport`: dossier contenant le rapport (version tex et pdf).
- `/results`: dossier contenant tous les résultats:
  - `/balzac_result`: contient les images des ngrams en fonction du nombre de ligne et de la taille du vocabulaire.
  - `/genius_results`: contient les images: nombre de mots par artistes et perplexité des modèles sur des textes d'artiste.
  - `/ngram`: contient l'ensemble des occurences des séquences.
- `/tools`: dossier contenant des scripts python permettant de bien formater les données. Il contient:
  - `masque.py`: ce fichier permet de créer les fichiers masks.
  - `merge_file.py`: ce fichier nous permet de réunir en un seul fichier texte l'ensemble de nos textes d'entraînement, de même pour nos textes de test, afin de simplifier le processus d'entraînement.
  - `preparation.py`: ce fichier nous permet de tokeniser un dossier de textes en une seule commande. 
  - `remove_first_line.py`: ce fichier nous permet de retirer l'entête superflue des fichiers textes des paroles des différents chanteurs séléctionnés dans la base de données Genius.
  - `space.py`: ce fichier permet de modifier les textes pour rajouter des espaces entre < s > et le premier mot, qui sont manquants parfois dans les données que nous avons choisies.
  - `splitCorpus.py`: ce fichier permet de rassembler un ensemble de textes et de créer deux fichiers train.txt et test.txt.
  - `tokenizer.py`: ce fichier permet de tokeniser un texte brut.
- `data.py`: permet de charger les données voulues.
- `ngram.py`: permet de créer des n-grams.
- `perplexite.py`: permet de calculer la perplexité d'un ngram entrainé sur un texte d'entrainement et de le tester sur un texte de test. 
- `devine.py`: prend un ngram et un contexte et prédit le mot suivant. 
- `genere.py`: permet de générer un texte à partir d'un input.
- `balzac.py`: calcule la perplexité des ngrams en fonction de la taille du corpus (avec une incrémentation de la taille du corpus de 1% à chaque étape).
- `genius.py`: entraîne un modèle ngram sur chaque artiste et regarde la perplexité sur des textes de ses artistes. On peut aussi utliser la MDS (Multidimensional scaling) pour projeter les artistes dans un espace de dimension 2.
- `tp_markov.pdf`: sujet du TP.
- `requierements.txt`: contient la liste de tous les packages python utilisés avec leur version. Faire `pip install -r requierements.txt` pour tout installer. Note: on a utlisé Python 3.9

## Exécution du code:

Nous avons fait en sorte que les fichiers python, se compose d'un ensemble de définition de fonction et puis
une liste d'éxécution dans un 
```python
if __name__ == '__main__':
```
Cela permet de faire toutes les excéutions de fonctions uniquement si vous exécutez ce fichier. 