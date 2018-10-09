# Retrofittingの導入
## ●環境
### jupyterで実行する
## ●ディレクトリ構成
```
.
├── README.md ・・・　このファイル
├── lexicons
│   ├── framenet.txt
│   ├── ppdb-xl.txt
│   ├── retrofitting
│   ├── wordnet-jpn.txt
│   ├── wordnet-synonyms+.txt
│   └── wordnet-synonyms.txt
├── wnjpn.db ・・・ wordnetのDB
├── preprocess.ipynb ・・・ wordnet辞書であるresult.txtの作成
├── result.txt ・・・ wordnet-jpn.txt
├── retrofitting.ipynb ・・・ retrofitting
├── out_vec.txt ・・・ retrofittingしたnewvec
├── eval.ipynb ・・・ WordSim評価，WordAnalogy評価をするファイル
├── word2vec
│   ├── out_vec.txt ・・・ newvec
│   └── vectors.model ・・・ 初期vec
├── wordAnalogy ・・・ WordAnalogy評価セット
│   └── questions-words.txt
└── wordsim353_sim_rel ・・・ WordSim評価セット
    ├── wordsim353_agreed.txt
    ├── wordsim353_annotator1.txt
    ├── wordsim353_annotator2.txt
    ├── wordsim_relatedness_goldstandard.txt
    └── wordsim_similarity_goldstandard.txt
```
## ●wordnetの辞書作成
```
preprocess.ipynbの実行
-> ./result.txtの作成
```
## ●retrofittingでnewvecの作成
```
retrofitting.ipynbの実行
-> ./newvec.txtの作成
```
## ●評価
```
eval.ipynbの実行
-> WordSim評価とwordAnalogy評価を行う
```
## ●結果（excel参照）
```
単語v1とv2の類似度をnewvecと初期のvecで算出し，差を求める．
さらに，それぞれの単語のwordnetにおける類義語リストのうち更新対象の単語，単語数を求める．
「差」と「v1とv2の更新対象の単語，単語数」に以下のような関係があった．
・単語v1とv2の更新対象の単語に被りのある場合，v1とv2の類似度は高くなる
・単語v1とv2の更新対象の単語数が10個以上あると，v1とv2の類似度はやや高くなる傾向にある
・単語v1とv2の更新対象の単語数が10個未満だと，v1とv2の類義語は低くなる傾向にある
・単語v1とv2の更新対象の単語において，一方が0個であると，v1とv2の類似度は低くなる傾向にある
```