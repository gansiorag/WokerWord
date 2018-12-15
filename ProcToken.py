'''
Created on 22 нояб. 2018 г.
модуль процесса токенитезации
@author: al
'''
import sys
import re
import rus_preprocessing_udpipe
import sqlite3
from ufal.udpipe import Model, Pipeline
#from rus_preprocessing_udpipe import *
def stopSqlite(isxStr):
      moderstr=isxStr
      moderstr = moderstr.replace('"',' ')
      moderstr = moderstr.replace('\'',' ')
      return moderstr 
def stopModel(isxStr):
      moderstr=isxStr
      moderstr = moderstr.replace('\"',' ')
      moderstr = moderstr.replace('\'',' ') 
      return moderstr        
def stopword(isxStr,stopWW):
    prstr=""
    moderstr=" "+isxStr
    moderstr=moderstr.lower()
    moderstr=re.findall(r'[а-я]+', moderstr)
    for kk in  moderstr:
      prstr += "{} ".format(kk)
    prstr=re.sub(r'\s[а-я][а-я]\s',' ',prstr) 
    prstr=re.sub(r'\s[а-я]\s',' ',prstr)
    prstr=re.sub(r'\s[a-z][a-z]\s',' ',prstr) 
    prstr=re.sub(r'\s[a-z,λ]\s',' ',prstr) 
    for wwi in stopWW:
        prstr = prstr.replace(' '+wwi+' ',' ')
    return prstr

def tokeniz(FileIsxText,FileVixText):
    output=["1","2"]
    udpipe_model_url = '/home/al/eclipse-work_cpp/Lingvo/isxDate/udpipe_syntagrus.model'  # URL of the UDPipe model
    #udpipe_filename = udpipe_model_url.split('/')[-1]
    FileStopWord='/home/al/eclipse-work_cpp/Lingvo/isxDate/stopword.csv'
    SpisStop=[]
    with open(FileStopWord) as fileStop:
        SpisStop = fileStop.read().splitlines()

    print('Loading the model...', file=sys.stderr)
    model = Model.load(udpipe_model_url)
    process_pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
    fileIsh = open(FileIsxText,'r')
    fileVix = sqlite3.connect(FileVixText)
    cursor = fileVix.cursor()
    print(FileIsxText, file=sys.stderr)
    print(FileVixText, file=sys.stderr)
    ishText = fileIsh.readline()
    while ishText:
        #ishText = fileIsh.readline()
        print (ishText, file=sys.stderr)
        ishText=stopSqlite(ishText)
        print (ishText, file=sys.stderr)
        isledText=ishText
        isledText=stopword(ishText, SpisStop)
        print (isledText, file=sys.stderr)
        output.clear()
        output=rus_preprocessing_udpipe.OsnToken(process_pipeline, isledText)
        print(output[:30], file=sys.stderr)
        #ishText = stopModel(ishText)
        #sql="INSERT INTO tizertext (text_ish,text_tok) VALUES (?,?)",(ishText,isledText)
        print (ishText, file=sys.stderr)
        print (isledText, file=sys.stderr)        
        cursor.execute("INSERT INTO tizertext (text_ish,text_tok) VALUES (?,?)",(ishText,isledText))
        sql="""select seq from sqlite_sequence where name='tizertext'"""
        iddtizer=cursor.execute(sql)
        id3=iddtizer.fetchone()[0]
        print (isledText, file=sys.stderr)
        print(id3,file=sys.stderr)
        print(output[:30], file=sys.stderr)
        for iir in output:
            #iir=stopModel(iir)
            cursor.execute("INSERT INTO ish_word (word_ish,id_tizertext) VALUES (?,?)",(iir,id3))
        fileVix.commit()
        ishText = fileIsh.readline()
    fileIsh.close()
    fileVix.close()
    
    