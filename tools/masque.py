import sys
import random

if len(sys.argv) < 3 :
    print("Usage:", sys.argv[0], "fichier_tokenisé","nombre_d'_exemples_à_générer")
    exit(0)

fileName = sys.argv[1]
nbExamples = int(sys.argv[2])

f = open(fileName, "r")
first = True
sentences = []
for line in f:
    tokens = line.split()
    if first:
        padding = 0
        while tokens[padding] == '<s>':
            padding += 1
        first = False
    sentences.append(tokens)

sentNb = len(sentences)
n = 0
alreadySelected = []
while n < nbExamples :
    sentenceIndex = random.randint(0, sentNb - 1)
    tokenPosition = random.randint(padding, len(sentences[sentenceIndex]) - padding - 1)
    tuple = (sentenceIndex, tokenPosition)
    if tuple not in alreadySelected:
        alreadySelected.append(tuple)
        print(tokenPosition, end = " ")
        for token in sentences[sentenceIndex]:
            print(token, end = ' ')
        print()
        n += 1
