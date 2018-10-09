# -*- coding: utf-8 -*-
# python3
#
import argparse
import gzip
import math
import numpy
import re
import sys
import numpy as np
from copy import deepcopy
import codecs

isNumber = re.compile(r'\d+.*')
def norm_word(word):
  if isNumber.search(word.lower()):
    return '---num---'
  elif re.sub(r'\W+', '', word) == '':
    return '---punc---'
  else:
    return word.lower()

"""Read all the word vectors and normalize them"""
def read_word_vecs(filename):
    wordVectors = {}
    # ファイル読み込み
    if filename.endswith('.gz'): 
        fileObject = gzip.open(filename, 'r')
    else: 
        fileObject = codecs.open(filename, "r", "utf-8", 'ignore')
        
    for line in fileObject:
        # line = line.strip().lower()
        line = line.strip()
        word = line.split()[0]
        wordVectors[word] = numpy.zeros(len(line.split())-1, dtype=float)
        for index, vecVal in enumerate(line.split()[1:]):
            wordVectors[word][index] = float(vecVal)
        """normalize weight vector"""
        wordVectors[word] /= math.sqrt((wordVectors[word]**2).sum() + 1e-6)

    sys.stderr.write("Vectors read from: "+filename+" \n")
    return wordVectors

"""Write word vectors to file"""
def print_word_vecs(wordVectors, outFileName):
    sys.stderr.write('\nWriting down the vectors in '+outFileName+'\n')
    outFile = open(outFileName, 'w')  
    for word, values in wordVectors.items():
        outFile.write(word+' ')
        for val in wordVectors[word]:
            outFile.write('%.4f' %(val)+' ')
        outFile.write('\n')      
    outFile.close()
  
"""Read the PPDB.etc word relations as a dictionary"""
def read_lexicon(filename):
    lexicon = {}
    fileObject = open(filename, 'r')
    for line in fileObject:
        words = line.lower().strip().split()
        lexicon[norm_word(words[0])] = [norm_word(word) for word in words[1:]]
    return lexicon

"""Retrofit word vectors to a lexicon"""
def retrofit(wordVecs, lexicon, numIters):
    # Input word vecs
    newWordVecs = deepcopy(wordVecs)
    # Input word vecsの単語リスト
    wvVocab = set(newWordVecs.keys())
    # wvVocabとlexiconの共通単語
    loopVocab = wvVocab.intersection(set(lexicon.keys()))

    for _ in range(numIters): #10回程度
        # loop through every node also in ontology (else just use data estimate)
        for word in loopVocab:
            # lexicon wordの近傍単語とwvVocabの共通単語とその個数
            wordNeighbours = set(lexicon[word]).intersection(wvVocab)
            numNeighbours = len(wordNeighbours)
            # no neighbours -> pass - use data estimate
            if numNeighbours == 0:
                continue
            """分散表現の更新手続き"""
            # the weight of the data estimate if the number of neighbours
            newVec = numNeighbours * wordVecs[word]
            # loop over neighbours and add to new vector (currently with weight 1)
            for ppWord in wordNeighbours:
                newVec += newWordVecs[ppWord]
            newWordVecs[word] = newVec/(2*numNeighbours)
    return newWordVecs

def similarity(v1, v2):
    n1 = np.linalg.norm(v1) # v1のノルム
    n2 = np.linalg.norm(v2) # v2のノルム
    return np.dot(v1, v2) / (n1*n2) # 内積 / 
  
if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", type=str, default=None, help="Input word vecs")
  parser.add_argument("-l", "--lexicon", type=str, default=None, help="Lexicon file name")
  parser.add_argument("-o", "--output", type=str, help="Output word vecs")
  parser.add_argument("-n", "--numiter", type=int, default=10, help="Num iterations")
  args = parser.parse_args()

  wordVecs = read_word_vecs(args.input)
  lexicon = read_lexicon(args.lexicon)
  numIter = int(args.numiter)
  outFileName = args.output
  
  """Enrich the word vectors using ppdb and print the enriched vectors"""
  new_vec = retrofit(wordVecs, lexicon, numIter)
  print_word_vecs(new_vec, outFileName)
