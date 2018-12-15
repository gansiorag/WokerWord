'''
Created on 29 нояб. 2018 г.

@author: al
'''
import sys
import gensim, logging
import sqlite3
from numpy import int

def sinonimModel(fileBaza,fileModel):
    #информация о работе
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO) 
    BazaAnaliz = sqlite3.connect(fileBaza)
    cursor = BazaAnaliz.cursor()
    print ("Загружаем модель", file=sys.stderr)
    #m = '/home/al/eclipse-work_cpp/Lingvo/isxDate/ruwikiruscorpora_upos_skipgram_300_2_2018.vec.gz'
    if fileModel.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(fileModel, binary=False)
    elif fileModel.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(fileModel, binary=True)
    else:
      model = gensim.models.Word2Vec.load(fileModel)
    print ("Модель загружена", file=sys.stderr)
    model.init_sims(replace=True)
    with BazaAnaliz:    
      cur = BazaAnaliz.cursor()
      #cur.execute("select distinct word_ish from ish_word where word_ish like '%_NOUN'")
      cur.execute("select distinct word_ish from ish_word")
      rowm= cur.fetchall()
      KolStr=int(len(rowm))
      print(KolStr, file=sys.stderr)
      indd=int(1)  
      while indd<KolStr:
            print("Word = ",indd)
            word=rowm[indd-int(1)][0]
            if word in model:
        # выдаем 10 ближайших соседей слова:
              for i in model.most_similar(positive=[word], topn=20):
            # слово + коэффициент косинусной близости
                print(i[0],i[1])
                cursor.execute("INSERT INTO model7 (word_ish,word_sin,ves) VALUES (?,?,?)",(word,i[0],str(i[1]),))
                #print('\n')
            else:
        # Увы!
                print(word + ' is not present in the model')
                cursor.execute("INSERT INTO model7 (word_ish,word_sin,ves) VALUES (?,?,?)",(word,"no model",str(0.0),))
            indd +=int(1)
            BazaAnaliz.commit()
    BazaAnaliz.close()  