'''
Created on 25 нояб. 2018 г.
Сравнение титлов и тизеров. Они читаются из баз и результат 
записывается в файл формата csv
@author: al
'''
import sys
import os
import sqlite3
from numpy import int

def SravnTitle_Tizer(FileTitle,FileRezult):
  #Открываем базу тайтлов и создаем все параметры
  spisok_znakTitle=['1','2']
  spisok_znakTizer=['1','2']
  FileTitleS = sqlite3.connect(FileTitle)
  FileTitlecursor = FileTitleS.cursor()
  idFileTitlecursor=FileTitlecursor.execute("select count(*) from tizertext")
  KolStrFileTitle=int(idFileTitlecursor.fetchone()[0]) 
  idFileTizercursor=FileTitlecursor.execute("select count(*) from t_tizertext")
  KolStrFileTizer=int(idFileTizercursor.fetchone()[0])
  
  #открываем файл для записи результатов
  file_rezult = open(FileRezult,'w')

  idTitl=int(0)
  #KolStrFileTitle=int(50)
  while idTitl<KolStrFileTitle:
    idTitl+=int(1)
    idFileTitlecursor=FileTitlecursor.execute("select word_sky from tizertext,ish_word,sky_word where tizertext.id=? and ish_word.id_tizertext=tizertext.id and sky_word.id_ish_word=ish_word.id",(str(idTitl),))  
    spisokTitle=idFileTitlecursor.fetchall()
    print (spisokTitle[:30], file=sys.stderr) 
    LenSpisokTitleSm=len(spisokTitle)
    
    idFileTitlecursor=FileTitlecursor.execute("select word_ish from ish_word where id_tizertext=?",(str(idTitl),))  
    spisokTitleZnak=idFileTitlecursor.fetchall()
    print (spisokTitleZnak[:30], file=sys.stderr) 
    
    spisok_znakTitle.clear()
    for tz in spisokTitleZnak:
        t_first=tz[0].split("_")
        spisok_znakTitle.append(t_first[0])
    idTizer=int(0)
    print (spisok_znakTitle[:30], file=sys.stderr)
    LenSpisokTitleZnak=len(spisok_znakTitle)
    #KolStrFileTizer=int(100)
    while idTizer<KolStrFileTizer:
      idTizer+=int(1)
      idFileTizercursor=FileTitlecursor.execute("select t_word_sky from t_tizertext,t_ish_word,t_sky_word where t_tizertext.t_id=? and t_ish_word.t_id_tizertext=t_tizertext.t_id and t_sky_word.t_id_ish_word=t_ish_word.t_id",(str(idTizer),))
      spisokTizerSm=idFileTizercursor.fetchall()
      print (spisokTizerSm[:30], file=sys.stderr)
      idFileTizercursor=FileTitlecursor.execute("select t_word_ish from t_ish_word where  t_id_tizertext=?",(str(idTizer),))
      spisokTizerZnak=idFileTizercursor.fetchall()

      spisok_znakTizer.clear()
      for tzt in spisokTizerZnak:
        t_firstt=(tzt[0].split("_"))
        spisok_znakTizer.append(t_firstt[0])
      print (spisok_znakTizer[:30], file=sys.stderr)
      
      resultSpisok_znak=list(set(spisok_znakTizer) & set(spisok_znakTitle))
      LenspisokZnak=len(resultSpisok_znak)
      rel_znak_title=float(LenspisokZnak)/float(LenSpisokTitleZnak)
      rel_znak_tizer=float(LenspisokZnak)/float(len(spisok_znakTizer))
      
      resultSpisok_Sm=list(set(spisokTizerSm) & set(spisokTitle))
      LenresultSpisokSm=len(resultSpisok_Sm)
      print (resultSpisok_Sm[:30], file=sys.stderr)      
      LenspisokTizerSm=len(spisokTizerSm)
      rel_sm_title=float(LenresultSpisokSm)/float(LenSpisokTitleSm)
      rel_sm_tizer=float(LenresultSpisokSm)/float(len(spisokTizerSm))    
                                                  
      rel_znak=max(rel_znak_title,rel_znak_tizer)
      rel_sm=max(rel_sm_title,rel_sm_tizer)
      
      file_rezult.write(str(idTitl)+";"+str(idTizer)+";"+str(rel_znak)+";"+str(rel_sm)+";"+str(rel_znak_title)+";"+str(rel_sm_title)+";"+str(rel_znak_tizer)+";"+str(rel_sm_tizer)+"\n")
  file_rezult.close()
  FileTitleS.close() 


  
  