# -*- coding: utf-8 -*-
# python3
#
import sqlite3
import sys
from collections import namedtuple
from pprint import pprint
import codecs

# DBにconnectする
conn = sqlite3.connect("./wnjpn.db")

# 単語をwordテーブルから探す
Word = namedtuple('Word', 'wordid lang lemma pron pos') 
def getWords(lemma):
    cur = conn.execute("select * from word where lemma=?", (lemma,))
    return [Word(*row) for row in cur]

# senseテーブルからwordが属するsynsetを抽出する
Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')
def getSenses(word):
    cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
    return [Sense(*row) for row in cur]

Synset = namedtuple('Synset', 'synset pos name src')
def getSynset(synset):
    cur = conn.execute("select * from synset where synset=?", (synset,))
    return Synset(*cur.fetchone())

def getWordsFromSynset(synset, lang):
    cur = conn.execute("select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;", (synset,lang))
    return [Word(*row) for row in cur]

# synonymの取得
def getWordsFromSenses(sense, lang="jpn"):
    synonym = {}
    for s in sense:
        lemmas = [] # synonymの単語
        syns = getWordsFromSynset(s.synset, lang)
        for sy in syns:
            lemmas.append(sy.lemma)
            synonym[getSynset(s.synset).name] = lemmas
    return synonym

# 同義語を取得する
def getSynonym(word):
    synonym = {}
    words = getWords(word)
    if words:
        for w in words:
            sense = getSenses(w)
            s = getWordsFromSenses(sense)
            synonym = dict(list(synonym.items()) + list(s.items()))
    return synonym

# 追加部分
# lang=jpnの収録単語を取得する
def getAllwords():
    Word = namedtuple('Word', 'wordid lang lemma pron pos') 
    cur = conn.execute("select word.* from word where word.lang=?", ('jpn',))
    Words = []
    for w in [Word(*row) for row in cur]:
        Words.append(w.lemma)
    return Words

"""Write word vectors to file"""
def print_word_vecs(wordVectors, outFileName):
    sys.stderr.write('\nWriting down the vectors in '+outFileName+'\n')
    outFile = open(outFileName, 'w')  
    for word, values in wordVectors.items():
        # keyを書き込む
        if len(wordVectors[word]) == 1 and word in values:
            pass
        else:
            outFile.write(word+' ')
            for val in wordVectors[word]:
                if val != word:
                    # valueを書き込む
                    outFile.write(str(val)+' ')
                else:
                    pass
            outFile.write('\n')      
    outFile.close()

if __name__ == '__main__':
    # 単語リストの取得
    word_list = getAllwords()
    # 同義語の取得と保存
    result = {}
    for one_word in word_list:
        value = []
        synonym = getSynonym(one_word)
        for eng in list(synonym.keys()):
            value.extend(synonym[eng])
        # 重複する単語を削除する（順序を保持する）
        value_unq = []
        for x in value:
            if x not in value_unq:
                value_unq.append(x)
        result[one_word] = value_unq
    print_word_vecs(result, './result.txt')
