'''
Created on 25 нояб. 2018 г.

@author: al
'''
import sys
import gensim, logging
import sqlite3
from numpy import int

def modelizm(fileBaza):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    BazaAnaliz = sqlite3.connect(fileBaza)
    cursor = BazaAnaliz.cursor()
    print ("Загружаем модель", file=sys.stderr)
    #m = '/home/al/eclipse-work_cpp/Lingvo/isxDate/ruwikiruscorpora_upos_skipgram_300_2_2018.vec.gz'
    m = '/home/al/eclipse-work_cpp/Lingvo/isxDate/ruscorpora_upos_skipgram_300_10_2017.bin.gz'
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
      model = gensim.models.Word2Vec.load(m)
    print ("Модель загружена", file=sys.stderr)
    model.init_sims(replace=True)
    with BazaAnaliz:    
      cur = BazaAnaliz.cursor()
      iddtizer=cur.execute("select count(*) from ish_word")
      KolStr=int(iddtizer.fetchone()[0])-int(1) 
      cur.execute("SELECT id,word_ish,id_tizertext FROM ish_word WHERE id=1")
      rowm= cur.fetchall()
      row=rowm[0][1]
      print(row, file=sys.stderr)
      indd=int(1)  
      while indd<KolStr:
            word=row
            print(word,"     ",word,word,word,word,)
            cursor.execute("INSERT INTO sky_word (word_sky,wes,id_ish_word) VALUES (?,?,?)",(word,str(1.0),str(indd),))
        # for word in words:
        # есть ли слово в модели? Может быть, и нет
            if word in model:
        # выдаем 10 ближайших соседей слова:
              for i in model.most_similar(positive=[word], topn=10):
            # слово + коэффициент косинусной близости
                print(i[0],i[1])
                cursor.execute("INSERT INTO sky_word (word_sky,wes,id_ish_word) VALUES (?,?,?)",(i[0],str(i[1]),str(indd),))
                #print('\n')
            else:
        # Увы!
                print(word + ' is not present in the model')
            indd +=int(1)
            cur.execute("SELECT id,word_ish,id_tizertext FROM ish_word WHERE id=?",(str(indd),))
            rowm= cur.fetchall()
            row=rowm[0][1]
            BazaAnaliz.commit()
    BazaAnaliz.close()   
        