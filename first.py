"""
Первая страница комплекса работы с текстом.
1. Процесс токенезации текста
2. Процесс лемматизации текста
3. Процесс создания облака слов которое порождают тайтлы
   а) токенезация тайтлов
   б) лемматизация тайтлов
   в) создание на w2v облака слов на основе выбранной модели и набора слов тайтлов
4. Процесс создания облака слов которое порождает тизеры
   а) токенезация тизеров
   б) лемматизация тизеров
   в) создание на w2v облака слов на основе выбранной модели и набора слов тизеров
5. Процесс расчета релевантности
   модель 1 
   модель 2
   модель 3
       расчет релевантности на основе похожести слов по существительным, глаголам, прилагательным
       сравниваются два облака облако тайтлов и облака тизеров 1. существительным (_NOUN) - по основанию по
       и по основанию по тизерам - какой процент выше тот и берется за процент релевантности
       2. глаголам (_VERB) так же как по существительным
       3.прилагательным (_ADJ) так же как по прилагательным
       Коэф.релев= Ves(NOUN)+Ves(VERB)+Ves(ADJ)

"""




from tkinter import *
from tkinter.filedialog import askopenfilename
import ProcToken
import WorkWithModel
import SravnTitleTizer
import SinonimModel
import ParserSite
import Lemmatiz
from tkinter import ttk
#from reportlab.platypus.paragraph import style
#from reportlab.lib.styles import LineStyle
#from reportlab.platypus.paragraph import 



""" 
расчет облака слов порождаемых словами тайтлов и записываемых в отдельную таблицу
в базе. модель тоже выбирается

def click_sinonim():
     FileIsxText=lineTextFileTizer.get('1.0', END+'-1c')
     #FileVixText=lineTextFileVihTitle.get('1.0', END+'-1c')
     print(FileIsxText, file=sys.stderr)
     SinonimModel.sinonimModel(FileIsxText)
"""

# P A G E 1
def Page1_click_buttonOpenTizer():
   Page1_lineTextFileTizer.delete(1.0,END)
   filenameTizer = askopenfilename()
   Page1_lineTextFileTizer.insert(1.0,filenameTizer)

def Page1_click_buttonOpenRezult():
     Page1_lineTextFileRezult.delete(1.0,END)
     filenameTizer = askopenfilename()
     Page1_lineTextFileRezult.insert(1.0,filenameTizer)
   
def Page1_click_tokeniz():
     FileIsxText=Page1_lineTextFileTizer.get('1.0', END+'-1c')
     FileVixText=Page1_lineTextFileRezult.get('1.0', END+'-1c')
     print(FileIsxText, file=sys.stderr)
     ProcToken.tokeniz(FileIsxText,FileVixText)


  
 # P A G E 2
    
def click_lemmatizacia_Open_Ish_Tekst():
     page2_lineTextFileIshFile.delete(1.0,END)
     filenameIsxText = askopenfilename()
     page2_lineTextFileIshFile.insert(1.0,filenameIsxText)
 
     
def click_lemmatizacia_Open_Rezult_Text():
      page2_lineTextFileRezultFile.delete(1.0,END)
      filenameRezult = askopenfilename()
      page2_lineTextFileRezultFile.insert(1.0,filenameRezult)
      
def click_lemmatizacia():
    FileIsxText=page2_lineTextFileIshFile.get('1.0', END+'-1c')
    FileLemma=page2_lineTextFileRezultFile.get('1.0', END+'-1c')
    Lemmatiz.LemmatizaciaText(FileIsxText, FileLemma)
     
     
  # P A G E 3   
       
def click_button_FileRezultBaza():
     page3_lineTextFileRezultBaza.delete(1.0,END)
     FileRezultBaza=askopenfilename()
     page3_lineTextFileRezultBaza.insert(1.0,FileRezultBaza)

def click_button_FileModel():
     page3_lineTextFileModel.delete(1.0,END)
     FileRezultBaza=askopenfilename()
     page3_lineTextFileModel.insert(1.0,FileRezultBaza)
     
def click_button_Res_Srav():
     FileBaza=page3_lineTextFileRezultBaza.get('1.0', END+'-1c')
     FileModel= page3_lineTextFileModel.get('1.0', END+'-1c')
     SinonimModel.sinonimModel( FileBaza,FileModel)
     
     # P A G E  4 Парасер сайта
#===============================================================================
# Парсер сайта. Кнопка выбора базы куда записываются ссылки с сайта
# Из базы беруться уникальные ссылки и парсятся тоже.
# Кнопка выбора файл куда записывается текст с сайта
# Окно текста куда надо ввести адрес сайта -  page4_lineTextAdresSite
#===============================================================================    
     
def page4_clik_ViborBazi():
      page4_lineTextVeborBazi.delete(1.0,END)
      FileRezultBaza=askopenfilename()
      page4_lineTextVeborBazi.insert(1.0,FileRezultBaza)     
     
def page4_clik_ViborFileRezult():    
       page4_lineTextFileRezult.delete(1.0,END)
       FileRezultBaza=askopenfilename()
       page4_lineTextFileRezult.insert(1.0,FileRezultBaza)

def page4_clik_Go_Parser():
     AdresSite=page4_lineTextAdresSite.get('1.0', END+'-1c')
     FileBaza=page4_lineTextVeborBazi.get('1.0', END+'-1c')
     FileModel= page4_lineTextFileRezult.get('1.0', END+'-1c')
     AdresSiteZn= page4_lineTextAdresSiteZn.get('1.0', END+'-1c')     
     ParserSite.parserSite( AdresSite,FileBaza,FileModel,AdresSiteZn)
     
 
if __name__ == "__main__": 
    root = Tk()
    root.title("Тизеры и тайтлы")
    root.geometry("1000x400+300+250")
    TablOsn = ttk.Notebook()
    page1=Frame(TablOsn,height = 3, width = 400)
    page2=Frame(TablOsn)
    page3=Frame(TablOsn)
    page4=Frame(TablOsn)
    page5=Frame(TablOsn)
    TablOsn.add(page1, text='Токенезация текста')
    TablOsn.add(page2, text='Лемматизация текста')
    TablOsn.add(page3, text='Создания облака слов по тайтлам')
    TablOsn.add(page4, text='Парсер ссылок сайта')
    TablOsn.add(page5, text='page5')
    
    TablOsn.pack(padx=2, pady=3, fill=BOTH, expand=1)
    
    # P A G E 1 Токенезация текста
    
    Page1_lineTextFileTizer=Text(page1)
    Page1_lineTextFileTizer.place(x=10, y=20, anchor="w", height=30, width=300, bordermode=OUTSIDE)
    Page1_btn_find_tizer = Button(page1,text="Выберите файл исходный", command=Page1_click_buttonOpenTizer)
    Page1_btn_find_tizer.place(x=315,y=20, anchor="w", height=30, width=250, bordermode=OUTSIDE)
       
   
    Page1_lineTextFileRezult=Text(page1)
    Page1_lineTextFileRezult.place(x=10,y=55,anchor="w",height=30,width=300)
    Page1_btn_OpenRezult = Button(page1,text="Выберите файл для результатов",command=Page1_click_buttonOpenRezult)   # текст кнопки 
    Page1_btn_OpenRezult.place(x=315, y=55, anchor="w", height=30, width=250, bordermode=OUTSIDE)
 

    Page1_btn_tokeniz = Button(page1,text="Сделать токенитизацию",command=Page1_click_tokeniz)
    Page1_btn_tokeniz.place(x=240,y=100, anchor="c", height=30, width=250, bordermode=OUTSIDE)


 
    
    
    # P A G E  2 Лемматизация текста

    page2_lineTextFileIshFile=Text(page2,font=12)
    page2_lineTextFileIshFile.place(x=10,y=20,anchor="nw",height=30,width=300)
    page2_btn_open_ishFile = Button(page2,text="Выберите файл исходного текста",command=click_lemmatizacia_Open_Ish_Tekst)
    page2_btn_open_ishFile.place(x=315, y=20, anchor="w", height=30, width=400, bordermode=OUTSIDE)
 
    page2_lineTextFileRezultFile=Text(page2,font=12)
    page2_lineTextFileRezultFile.place(x=10,y=90,anchor="w",height=30,width=300)
    page2_btn_open_RezultFile = Button(page2,text="Выберите файл для записи результатов",command=click_lemmatizacia_Open_Rezult_Text)
    page2_btn_open_RezultFile.place(x=315, y=90, anchor="w", height=30, width=400, bordermode=OUTSIDE)
 
    page2_btn_Lemmatizacia = Button(page2,text="Провести лемматизацию", command=click_lemmatizacia)
    page2_btn_Lemmatizacia.place(x=105, y=125, anchor="w", height=30, width=250, bordermode=OUTSIDE) 
 
     
    # P A G E  3 Создания облака слов по тайтлам
        
    page3_lineTextFileRezultBaza=Text(page3,font=12)
    page3_lineTextFileRezultBaza.place(x=10,y=20,anchor="w",height=30,width=300)
    btn_File_Resalt_Sravn = Button(page3,text="Выберите базу для записи результатов.",command=click_button_FileRezultBaza)   
    btn_File_Resalt_Sravn.place(x=315, y=20, anchor="w", height=30, width=400, bordermode=OUTSIDE)

    page3_lineTextFileModel=Text(page3,font=12)
    page3_lineTextFileModel.place(x=10,y=55,anchor="w",height=30,width=300)
    btn_File_Model = Button(page3,text="Выберите файл модели *.gz.",command=click_button_FileModel)   
    btn_File_Model.place(x=315, y=55, anchor="w", height=30, width=400, bordermode=OUTSIDE)
    
    btn_Resalt_Sravn = Button(page3,text="Рассчитать облако слов.",command=click_button_Res_Srav)   
    btn_Resalt_Sravn.place(x=150, y=125, anchor="center", height=30, width=250, bordermode=OUTSIDE)
    
    

    
  
    # P A G E  4 Парасер сайта
#===============================================================================
# Парсер сайта. Вводится его адрес сайта. Вводится база куда будут записываться ссылки сайта
# Из базы беруться уникальные ссылки и парсятся тоже.
# В файл записывается текст с сайта
#
#===============================================================================
    
    prezentText=""" Парсер сайта. Вводится его 
                    адрес сайта. Вводится база 
                    куда будут записываться 
                    ссылки сайта.Из базы 
                    беруться уникальные 
                    ссылки и парсятся тоже. 
                    В файл записывается 
                    текст с сайта"""
    page4_lineTextAdresSite=Text(page4,font=12)
    page4_lineTextAdresSite.insert(1.0,"http://")
    page4_lineTextAdresSite.place(x=10,y=20,anchor="w",height=30,width=300)
    page4_label_AdresSite=Label(page4, text="Введите адрес сайта",font=12)
    page4_label_AdresSite.place(x=315,y=20,anchor="w",height=30,width=250)  
       
    page4_label_Prezent=Label(page4, text=prezentText,font=12)
    page4_label_Prezent.place(x=565,y=30,anchor="w",height=600,width=300)
    
    page4_lineTextVeborBazi=Text(page4,font=12)
    page4_lineTextVeborBazi.place(x=10,y=55,anchor="w",height=30,width=300)    
    page4_btn_VeborBazi = Button(page4,text="Выберите базу результатов",command=page4_clik_ViborBazi)   
    page4_btn_VeborBazi.place(x=315, y=55, anchor="w", height=30, width=250, bordermode=OUTSIDE)
    
    page4_lineTextFileRezult=Text(page4,font=12)
    page4_lineTextFileRezult.place(x=10,y=85,anchor="w",height=30,width=300)    
    page4_btn_FileRezult = Button(page4,text="Выберите для записи текстов",command=page4_clik_ViborFileRezult)   
    page4_btn_FileRezult.place(x=315, y=85, anchor="w", height=30, width=250, bordermode=OUTSIDE)
    
    page4_btn_Go_Parser = Button(page4,text="Запустить парсер",command=page4_clik_Go_Parser)
    page4_btn_Go_Parser.place(x=200, y=125, anchor="w", height=30, width=150, bordermode=OUTSIDE)
    
    page4_lineTextAdresSiteZn=Text(page4,font=12)
    page4_lineTextAdresSiteZn.place(x=10,y=155,anchor="w",height=30,width=300)
    page4_label_AdresSiteZn=Label(page4, text="Введите сокращенный адрес сайта",font=12)
    page4_label_AdresSiteZn.place(x=315,y=155,anchor="w",height=30,width=250)  
    
    
root.mainloop()  

  
"""    
    # P A G E  5
    
    lineTextFileOpenSlov=Text(page5,font=12)
    lineTextFileOpenSlov.place(x=10,y=125,anchor="nw",height=30,width=300)
    
    btn_vib_slov = Button(page5,ext="Подключите словарь",          # текст кнопки 
             background="#555",     # фоновый цвет кнопки
             foreground="#ccc",     # цвет текста
             font="12"              # высота шрифта
             ,command=click_button_Op_Slov)
    btn_vib_slov.place(x=315, y=125, anchor="nw", height=30, width=250, bordermode=OUTSIDE)
"""

    
    