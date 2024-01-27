from typing import Tuple, List, Dict

from data import getfile_dumas, openfile
from ngram import ngram


def get_question(line: List[str], n_gram: int) -> Tuple[list[str], str]:
    """
    prend une ligne en argument et le n de ngram et revoie la liste des mots pour que le ngram devine le prochaine mot et la réponse.
    le premier élément de la ligne doit être un enter sous forme de str
    """
    assert 1 <= n_gram <= 3, "ngram doit être compris entre 1 et 3"

    index = int(line[0]) + 1
    return tuple(line[index + 1 - n_gram : index]), line[index]
    

def devine(question: Tuple[str], dico_train: Dict[str, int]) -> str:
    """
    Prend un tupple et regarde dans le dico_train, et renvoie le mot tq
        - question + mot est dans le dictnionaire
        - mot = argmax value(dico[question + mot])
    """
    len_question = len(question)

    if len_question == 0:
        sorted_dict = sorted(dico_train.items(), key=lambda x:-x[1])
        return sorted_dict[0][0]
    
    best_sequence, value = '<s>', 0 
    for key in dico_train.keys():
        if key[:len_question] == question and dico_train[key] > value:
            best_sequence = key
            value = dico_train[key]
    
    return best_sequence[-1]  


def devine_accuracy(file_train: str, file_mask: str, n_gram: int) -> float:
    """
    Renvoie l'accuracy du ngram entraîné sur file_train, testé sur file_mask
    """
    text_train = openfile(file_train)
    dico_train = ngram(text_train, n_gram)
    del text_train

    text_mask = openfile(file_mask, line_by_line=True)
    accuracy = 0
    for line in text_mask:
        question, reponse = get_question(line, n_gram=n_gram)
        predict = devine(question, dico_train)
        if reponse == predict:
            accuracy += 1
    return accuracy / len(text_mask)


if __name__ == '__main__':
    for i in range(5):
        file_mask = getfile_dumas(mode='test', mask=True)[i]
        file_train = getfile_dumas(mode='train')[i]
        print(f"train:{file_train} - mask:{file_mask}")
        for n_gram in range(1, 4):
            acc = devine_accuracy(file_train, file_mask, n_gram)
            print(f"accuracy of {n_gram}-gram: {acc}")
