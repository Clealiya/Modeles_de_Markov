import os
import subprocess

auteur = "balzac"

def tokennisation(folder_path: str, tokenized_folder_path: str):
    """
    Définition du dossier contenant les oeuvres de l'auteur en question / Création du dossier pour les fichiers tokenisés
    """
    # Si le dossier pour fichiers tokenisés n'existent pas, le créer
    if not os.path.exists(tokenized_folder_path):
        os.mkdir(tokenized_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # Enlever l'extension
            title = os.path.splitext(filename)[0]

            # Enleve les chiffres et remplace les - par des _
            title = title.split("_", 1)[-1].replace("-", "_")

            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(tokenized_folder_path, title + '.tok.txt')
            command = f"python tokenizer.py {input_file} {output_file} 2"

            # Execution de la commande
            process = subprocess.Popen(command, shell=True)
            process.wait()

            if process.returncode == 0:
                print(f"Tokenization complétée pour {filename}")
            else:
                print(f"Tokenization échouée pour {filename}")

    print("Tokenization process completed.")


if __name__ == "__main__":
    data_path = os.path.join('..', 'data')

    # tokennnized balzac data
    balzac_folder = os.path.join(data_path, 'balzac')
    tokenized_balzac_folder = balzac_folder + '_tokenized'
    if 'balzac_tokenized' not in os.listdir(data_path):
        tokennisation(balzac_folder, tokenized_balzac_folder)
    else:
        print('balzac already tokennized')

    # tokennnized genius lyrics
    genius_folder = os.path.join(data_path, 'genius_lyrics')
    tokenized_genius_folder = genius_folder + '_tokenized'
    if not os.path.exists(tokenized_genius_folder):
        os.mkdir(tokenized_genius_folder)

    if len(os.listdir(tokenized_genius_folder)) <= 3:
        for artist in os.listdir(genius_folder):
            tokennisation(folder_path=os.path.join(genius_folder, artist),
                          tokenized_folder_path=os.path.join(tokenized_genius_folder, artist))
    else:
        print('genius already tokennized')
    