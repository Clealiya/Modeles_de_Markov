import sys
import random

if len(sys.argv) < 5:
    print("Usage:", sys.argv[0], "fichier_tokenisé","ratio_corpus_test", "corpus_train", "corpus_test")
    exit(0)

corpusName = sys.argv[1]
test_ratio = float(sys.argv[2])
trainCorpusName = sys.argv[3]
testCorpusName = sys.argv[4]

print("processing file : ", corpusName)
fi = open(corpusName,'r')

totalWords = 0
sentenceArray = []
for sentence in fi:
    if sentence != "\n":
        sentenceArray.append(sentence)
        totalWords += len(sentence)
fi.close()

print("corpus size (in tokens) : ", totalWords)

sentenceNb = len(sentenceArray)

target = int(totalWords * test_ratio)
print("target size of test corpus (in tokens) : ", target)

testCorpus = []

wordNbInTest = 0
while(wordNbInTest < target):
    n = random.randint(0, sentenceNb - 1)
    if len(sentenceArray[n]) != 0 :
        wordNbInTest += len(sentenceArray[n])
        testCorpus.append(sentenceArray[n])
        sentenceArray[n] = ""

print("actual size of test corpus (in tokens) : ", wordNbInTest)
        
TrainFile =  open(trainCorpusName,'w')
for sentence in sentenceArray:
    if sentence != ""  :
        TrainFile.write(sentence)
TrainFile.close()
    
TestFile = open(testCorpusName,'w')
for sentence in testCorpus:
    TestFile.write(sentence)
TestFile.close()

    
