from gensim.models import word2vec
from gensim.test.utils import datapath
from gensim.models import KeyedVectors
from pyemd import emd
from gensim.similarities import WmdSimilarity
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import sqlite3
from sqlite3 import Cursor
from tkinter import messagebox 


name_vector=""

heighY=100

# page1 Начальные установки click Buttom
def page1_click_btn_Slovar():
    page1_lineTextFileSlovar.delete(1.0,END)
    global name_slovar
    name_slovar=askopenfilename(filetypes=(("DB files", "*.db"),("All files", "*.*") ))
    page1_lineTextFileSlovar.insert(1.0,name_slovar)
        
def page1_click_btn_Vector():
    page1_lineTextFileVector.delete(1.0,END)
    name_vector=askopenfilename(filetypes =(("BIN files","*.bin"),("All files", "*.*") ))
    page1_lineTextFileVector.insert(1.0,name_vector)
    global wv
    wv = KeyedVectors.load_word2vec_format(datapath(name_vector), binary=True) 

# page2 Контекстный анализ слов click Buttom
def page2_click_btn_Kontext():
    pole1=int(20)
    pole2=int(7)
    #количество слов 
    kolslov=int(page2_lineText_KolSlovo.get('1.0',END+'-1c'))
    slovo=page2_lineText_IshSlovo.get('1.0',END+'-1c')
    slovo=slovo.replace(' ','')
    baza_slovar=sqlite3
    baza_slovar=sqlite3.connect(name_slovar)
    cursorSlovar=baza_slovar.cursor()
    cursorSlovar.execute("select slovo, chast from slovos where slovo like '"+slovo+"%';")
    slugSpis=cursorSlovar.fetchone()
    if slugSpis is None:
        messagebox.showinfo("Слова нет в словаре корпуса.","Введите другое слово.")
    else:
        page2_lineText_TextData.delete(1.0,END)
        strD1=str(slugSpis[0])
        strD1=strD1.rjust(pole1," ")+" | "
        strD2="{:.4f}".format(float(1.0))
        strD2=strD2.ljust(pole2," ")+"| "
        strD3=str(slugSpis[1])
        strD3=strD3.ljust(pole2," ")+" |\n"
        page2_lineText_TextData.insert(INSERT,strD1+strD2+strD3)
        result=wv.most_similar(positive=[str(slugSpis[0])],topn=kolslov)
        for strTab in result:
            strD1=str(strTab[0])
            strD1=strD1.rjust(pole1," ")+" | "
            strD2="{:.4f}".format(float(strTab[1]))
            strD2=strD2.ljust(pole2," ")+"| "
            cursorSlovar.execute("select slovo, chast from slovos where slovo like '"+str(strTab[0])+"%';")
            slugSpis=cursorSlovar.fetchone()
            strD3=str((slugSpis[1]))
            strD3=strD3.ljust(pole2," ")+" |\n"
            page2_lineText_TextData.insert(INSERT,strD1+strD2+strD3)


# page2 Рассчет расстояния между словами

def page2_click_btn_Ras():
    pole1=int(20)
    pole2=int(7)
    slovo=page2_lineText_IshSlovo.get('1.0',END+'-1c')
    slovo=slovo.replace(' ','')
    dublslovo=page2_lineText_DublSlovo.get('1.0',END+'-1c')
    dublslovo=dublslovo.replace(' ','')
    baza_slovar=sqlite3
    baza_slovar=sqlite3.connect(name_slovar)
    cursorSlovar=baza_slovar.cursor()
    cursorSlovar.execute("select slovo, chast from slovos where slovo like '"+slovo+"%';")
    slugSpis1=cursorSlovar.fetchone()
    cursorSlovar.execute("select slovo, chast from slovos where slovo like '"+dublslovo+"%';")
    slugSpis2=cursorSlovar.fetchone()    
    if slugSpis1 is None:
        messagebox.showinfo("Слова 1 нет в словаре.","Введите другое слово.")
    if slugSpis2 is None:
        messagebox.showinfo("Слова 2 нет в словаре.","Введите другое слово.")      
    if (not(slugSpis1 is None) and not(slugSpis2 is None)):
        result=wv.distance(w1=str(slugSpis1[0]),w2=str(slugSpis2[0]))
        page2_lineText_TextData.delete(1.0,END)
        strD1="Расстояние между словами  \n" 
        strD2=str(slugSpis1[0])+ " \n"
        strD3=str(slugSpis2[0])+ " \n"
        strD4=" = "+ str(result)
        page2_lineText_TextData.insert(INSERT,strD1+strD2+strD3+strD4)
     
# page3  Контекстный анализ предложений
def page3_click_btn_Kontext():
    slugSpis1=[]
    slugSpis2=[]
    slugSpis3=[]
    result=""
    #лишнее слово
    predl=page3_lineText_IshPredl.get('1.0',END+'-1c')
    slovos=predl.split()
    for slovo in slovos:
         slovo.replace(' ','')
    baza_slovar=sqlite3
    baza_slovar=sqlite3.connect(name_slovar)
    cursorSlovar=baza_slovar.cursor()
    slugSpis2.clear()
    for slovo in slovos:
            cursorSlovar.execute("select slovo, chast from slovos where slovo like '"+slovo+"%';")
            slugSpis1=cursorSlovar.fetchone()
            if slugSpis1 is None:
              messagebox.showinfo("Слова "+slovo+" нет в словаре корпуса.","Введите другое слово.")
              break
            else:
              slugSpis2.append(slugSpis1)
    if len(slugSpis2)==len(slovos):
          for slovo in slugSpis2:
              slugSpis3.append(slovo[0])
          result=wv.doesnt_match(slugSpis3)
          page3_lineText_TextData.delete(1.0,END)    
          strD1="Лишнее слово в предложении - "
          page3_lineText_TextData.insert(INSERT,strD1+result)
        



# Определить пошожесть фраз
def page3_click_btn_Ras():
    slugSpis1=[]
    slugSpis2=[]
    slugSpis3=[]
    slugSpis4=[]
    #расстояние между фразами
    predl1=page3_lineText_IshPredl.get('1.0',END+'-1c')
    predl2=page3_lineText_DublPredl.get('1.0',END+'-1c')
    slovos=predl1.split()
    for slovo in slovos:
         slovo.replace(' ','')
    baza_slovar=sqlite3
    baza_slovar=sqlite3.connect(name_slovar)
    cursorSlovar=baza_slovar.cursor()
    #обрабатываем предложение 1
    slugSpis2.clear()
    for slovo in slovos:
            cursorSlovar.execute("select slovo, chast from slovos where slovo like '"+slovo+"%';")
            slugSpis1=cursorSlovar.fetchone()
            if slugSpis1 is None:
              messagebox.showinfo("Слова "+slovo+" нет в словаре корпуса.","Введите другое слово.")
              break
            else:
              slugSpis2.append(slugSpis1)
    if len(slugSpis2)==len(slovos):
          for slovo in slugSpis2:
              slugSpis3.append(slovo[0])
    #обрабатываем предложение 1          
    slovos=predl2.split()
    for slovo in slovos:
         slovo.replace(' ','')
    baza_slovar=sqlite3
    baza_slovar=sqlite3.connect(name_slovar)
    cursorSlovar=baza_slovar.cursor()
    slugSpis2.clear()
    for slovo in slovos:
            cursorSlovar.execute("select slovo, chast from slovos where slovo like '"+slovo+"%';")
            slugSpis1=cursorSlovar.fetchone()
            if slugSpis1 is None:
              messagebox.showinfo("Слова "+slovo+" нет в словаре корпуса.","Введите другое слово.")
              break
            else:
              slugSpis2.append(slugSpis1)
    if len(slugSpis2)==len(slovos):
          for slovo in slugSpis2:
              slugSpis4.append(slovo[0])
           
          result1=wv.wmdistance(slugSpis3, slugSpis4)
          page3_lineText_TextData.delete(1.0,END)    
          strD1="Расстояние между фразами - "
          page3_lineText_TextData.insert(INSERT,strD1+"{:.4f}".format(result1))





if __name__=="__main__":
    root=Tk()
    root.title("Контекстный анализ слов и коротких фраз")
    root.geometry("1000x500")
    mainmenu=Menu(root)
    root.config(menu=mainmenu)
    filemenu=Menu(mainmenu,tearoff=0)
    filemenu.add_command(label="Открыть...")
    filemenu.add_command(label="Новый")
    filemenu.add_command(label="Сохранить...")
    filemenu.add_command(label="Выход")
    
    helpmenu=Menu(mainmenu,tearoff=0)
    helpmenu.add_command(label="Помощь")
    helpmenu.add_command(label="О программе")
 

    mainmenu.add_cascade(label="Файл",menu=filemenu)
    mainmenu.add_cascade(label="Справка", menu=helpmenu)
    
    Osn=ttk.Notebook()
    page1=Frame(Osn)
    page2=Frame(Osn)
    page3=Frame(Osn)
    Osn.add(page1,text='  Начальные установки  ')  
    Osn.add(page2,text='  Контекстный анализ слов  ')
    Osn.add(page3,text='  Контекстный анализ коротких фраз  ')
    Osn.pack(padx=2,pady=3,fill=BOTH,expand=1)
    
    # page1 Начальные установки
    page1_lineTextFileSlovar=Text(page1)
    page1_lineTextFileSlovar.place(x=10, y=heighY, anchor="w", heigh=30,width=400,bordermode=OUTSIDE)

    page1_btn_Slovar=Button(page1,text="Выберите файл словаря",command=page1_click_btn_Slovar)
    page1_btn_Slovar.place(x=415, y=heighY, anchor="w", heigh=30,width=300,bordermode=OUTSIDE)

    page1_lineTextFileVector=Text(page1)
    page1_lineTextFileVector.place(x=10, y=heighY+50, anchor="w", heigh=30,width=400,bordermode=OUTSIDE)

    page1_btn_Vector=Button(page1,text="Выберите файл вектора",command=page1_click_btn_Vector)
    page1_btn_Vector.place(x=415, y=heighY+50, anchor="w", heigh=30,width=300,bordermode=OUTSIDE)

    # page2 Контекстный анализ слов
    page2_lineText_KolSlovo=Text(page2)
    page2_lineText_KolSlovo.place(x=10, y=heighY-50, anchor="w", heigh=30,width=35,bordermode=OUTSIDE)
    page2_lineText_KolSlovo.insert(1.0,"20")

    page2_label_Kol_Slovo=Label(page2,text="Количество слов в выдаче. По умолчанию 20")
    page2_label_Kol_Slovo.place(x=45, y=heighY-50, anchor="w", heigh=30,width=350,bordermode=OUTSIDE)                             

    page2_label_Nom1_Slovo=Label(page2,text="Слово 1")
    page2_label_Nom1_Slovo.place(x=20, y=heighY-20, anchor="w", heigh=20,width=100,bordermode=OUTSIDE)
    
    page2_lineText_IshSlovo=Text(page2)
    page2_lineText_IshSlovo.place(x=10, y=heighY, anchor="w", heigh=30,width=200,bordermode=OUTSIDE)

    page2_btn_Kontext=Button(page2,text="Показать контекст слова",command=page2_click_btn_Kontext)
    page2_btn_Kontext.place(x=215, y=heighY, anchor="w", heigh=30,width=200,bordermode=OUTSIDE)

    page2_label_Nom2_Slovo=Label(page2,text="Слово 2")
    page2_label_Nom2_Slovo.place(x=20, y=heighY+30, anchor="w", heigh=20,width=100,bordermode=OUTSIDE)
    
    page2_lineText_DublSlovo=Text(page2)
    page2_lineText_DublSlovo.place(x=10, y=heighY+50, anchor="w", heigh=30,width=200,bordermode=OUTSIDE)

    page2_btn_Ras=Button(page2,text="Рассчитать расстояние между словами",command=page2_click_btn_Ras)
    page2_btn_Ras.place(x=10, y=heighY+100, anchor="w", heigh=30,width=300,bordermode=OUTSIDE)

    page2_lineText_TextData=Text(page2)
    page2_lineText_TextData.place(x=450, y=heighY-90, anchor="nw", heigh=360,width=500,bordermode=OUTSIDE)

    # page3 Контекстный анализ предложений
    """
    page3_lineText_KolSlovo=Text(page3)
    page3_lineText_KolSlovo.place(x=10, y=heighY-50, anchor="w", heigh=30,width=35,bordermode=OUTSIDE)
    page3_lineText_KolSlovo.insert(1.0,"20")

    page3_label_Kol_Slovo=Label(page3,text="Количество слов в выдаче. По умолчанию 20")
    page3_label_Kol_Slovo.place(x=45, y=heighY-50, anchor="w", heigh=30,width=350,bordermode=OUTSIDE)                             
    """
    #Ввод первого предложения
    page3_label_Nom1_Predl=Label(page3,text="Предложение 1")
    page3_label_Nom1_Predl.place(x=20, y=heighY-20, anchor="w", heigh=20,width=120,bordermode=OUTSIDE)
    
    page3_lineText_IshPredl=Text(page3)
    page3_lineText_IshPredl.place(x=10, y=heighY, anchor="w", heigh=30,width=400,bordermode=OUTSIDE)

    page3_btn_Kontext=Button(page3,text="Показать лишние слово",command=page3_click_btn_Kontext)
    page3_btn_Kontext.place(x=415, y=heighY, anchor="w", heigh=30,width=200,bordermode=OUTSIDE)

    #Ввод второго предложения    
    page3_label_Nom2_Predl=Label(page3,text="Предложение 2")
    page3_label_Nom2_Predl.place(x=20, y=heighY+30, anchor="w", heigh=20,width=120,bordermode=OUTSIDE)
    
    page3_lineText_DublPredl=Text(page3)
    page3_lineText_DublPredl.place(x=10, y=heighY+50, anchor="w", heigh=30,width=400,bordermode=OUTSIDE)

    page3_btn_Ras=Button(page3,text="Рассчитать расстояние между предлжениями",command=page3_click_btn_Ras)
    page3_btn_Ras.place(x=10, y=heighY+100, anchor="w", heigh=30,width=400,bordermode=OUTSIDE)

    #Поле вывода результата
    page3_lineText_TextData=Text(page3)
    page3_lineText_TextData.place(x=620, y=heighY-90, anchor="nw", heigh=360,width=300,bordermode=OUTSIDE)
    
    
  

root.mainloop()
