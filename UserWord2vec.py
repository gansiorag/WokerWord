##############################################################################
#  Программа для демонстрации возможности алгоритма word2vec анализа текстов
#  1. Находит слова близкие по смыслу заданному слову
#  2. Находит лишнее по смыслу слово в предложении
#  3. Находит расстояние между двумя предложениями
#  4. Выбирает по образцу предложения из набора текстов наиболее
#     подходящий текст.
#  Для работы требуется файл с подготовленным вектором слов,
#  словарь вектора слов, файл лемматического словаря,
#  файл стоп слов, файл с набором предложений из которых надо выбирать.
#  подсчитывает время выполнения алгоритма
#  01.12.2018
#  @author: Alexander Gansior
###############################################################################

from gensim.test.utils import datapath
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import wordproc as wp


global lexdata # данные необходимые для обработки текста

# page1 Начальные установки click Buttom
# Загружаем словарь темы

def page1_click_btn_Slovar():
    page1_lineTextFileSlovar.delete(1.0, END)
    global name_slovar
    name_slovar = askopenfilename(filetypes=(("VOC files", "*.voc"), ("All files", "*.*")))
    page1_lineTextFileSlovar.insert(1.0, name_slovar)
    lexdata.slovar = wp.load_slovar(name_slovar)


# page1 Загружаем вектор
def page1_click_btn_Vector():
    page1_lineTextFileVector.delete(1.0, END)
    name_vector = askopenfilename(filetypes=(("BIN files", "*.bin"), ("All files", "*.*")))
    page1_lineTextFileVector.insert(1.0, name_vector)
    lexdata.wv.load_word2vec_format(datapath(name_vector), binary=True)


# page1 Загружаем лемматизатор
def page1_clic_btn_Lemmatisator():
    page1_lineTextFileLemat.delete(1.0, END)
    name_lemmat = askopenfilename(filetypes=(("lem files", "*.zip"), ("All files", "*.*")))
    page1_lineTextFileLemat.insert(1.0, name_lemmat)
    lexdata.lemmatizator = wp.load_lemmatizator(name_lemmat)


# page1 загружаем стоп слова
def page1_clic_btn_Stop():
    page1_lineTextStop.delete(1.0, END)
    name_stop = askopenfilename(filetypes=(("sts files", "*.sts"), ("All files", "*.*")))
    page1_lineTextStop.insert(1.0, name_stop)
    lexdata.slovoStop = wp.load_stopSlova(name_stop)


# page1 загружаем массив тизеров сразу их обрабатываем (токенезируем и лемматизируем)
def page1_clic_btn_Tizer():
    page1_lineTextTizer.delete(1.0, END)
    name_tiz = askopenfilename(filetypes=(("tiz files", "*.tiz"), ("All files", "*.*")))
    page1_lineTextTizer.insert(1.0, name_tiz)
    tizers = []
    row = []
    ishfile = open(name_tiz, 'r')
    ishtxt = ishfile.readline()
    kstr = 0
    while ishtxt:
        ishtxt1 = wp.tocenizator(ishtxt,lexdata.slovoStop, lexdata.rullmas)
        ishtxt1 = wp.lemmatizatorPred(ishtxt1,lexdata.lemmatizator)
        row.clear()
        tizers.append([])
        tizers[kstr].append(ishtxt)
        tizers[kstr].append(ishtxt1.strip())
        ishtxt = ishfile.readline()
        # print(tizers[kstr][0],tizers[kstr][1])
        kstr += 1
        if kstr == 250: break
    lexdata.AllTizer = tizers
    lexdata.kolTiz = kstr


# page2 Контекстный анализ слов click Buttom
def page2_click_btn_Kontext():
    pole1 = int(20)
    pole2 = int(7)
    # количество слов
    kolslov = int(page2_lineText_KolSlovo.get('1.0', END + '-1c'))
    porog = int(page2_lineText_Porog.get('1.0', END + '-1c'))
    slovo = page2_lineText_IshSlovo.get('1.0', END + '-1c')
    slovo = slovo.strip()
    if lexdata.lemmatizator.get(slovo) is None:
        messagebox.showinfo("Слова нет в словаре корпуса.", "Введите другое слово.")
    else:
        lemSlovo = lexdata.lemmatizator.get(slovo)
        if lexdata.slovar.get(lemSlovo) is None:
            messagebox.showinfo("Слова нет в словаре корпуса.", "Введите другое слово.")
        else:
            page2_lineText_TextData.delete(1.0, END)
            strD1 = str(lemSlovo)
            strD1 = strD1.rjust(pole1, " ") + " | "
            strD2 = "{:.4f}".format(float(1.0))
            strD2 = strD2.ljust(pole2, " ") + "| "
            strD3 = str(lexdata.slovar.get(lemSlovo))
            strD3 = strD3.ljust(pole2, " ") + " |\n"
            page2_lineText_TextData.insert(INSERT, strD1 + strD2 + strD3)
            result = lexdata.wv.most_similar(positive=[str(lemSlovo)], topn=100)
            ikprn = 0
            for strTab in result:
                strD1 = str(strTab[0])
                strD1 = strD1.rjust(pole1, " ") + " | "
                strD2 = "{:.4f}".format(float(strTab[1]))
                strD2 = strD2.ljust(pole2, " ") + "| "
                strD3 = str(lexdata.slovar.get(str(strTab[0])))  # получаем частоту из словаря
                strD3 = strD3.ljust(pole2, " ") + " |\n"
                pp = int(lexdata.slovar.get(str(strTab[0])))
                if (pp > porog and ikprn < kolslov):
                    page2_lineText_TextData.insert(INSERT, strD1 + strD2 + strD3)
                    ikprn = ikprn + 1


# page2 Рассчет расстояния между словами

def page2_click_btn_Ras():
    pole1 = int(20)
    pole2 = int(7)
    slovo = page2_lineText_IshSlovo.get('1.0', END + '-1c')
    slovo = slovo.strip()
    dublslovo = page2_lineText_DublSlovo.get('1.0', END + '-1c')
    dublslovo = dublslovo.strip()
    if lexdata.lemmatizator.get(slovo) is None or lexdata.lemmatizator.get(dublslovo) is None:
        if lexdata.lemmatizator.get(slovo) is None:
            messagebox.showinfo("Слова " + slovo + " нет в словаре корпуса.", "Введите другое слово.")
        if lexdata.lemmatizator.get(dublslovo) is None:
            messagebox.showinfo("Слова " + dublslovo + " нет в словаре корпуса.", "Введите другое слово.")
    else:
        if lexdata.slovar.get(lexdata.lemmatizator.get(slovo)) is None:
            messagebox.showinfo("Слова 1 нет в словаре.", "Введите другое слово.")
        if lexdata.slovar.get(lexdata.lemmatizator.get(dublslovo)) is None:
            messagebox.showinfo("Слова 2 нет в словаре.", "Введите другое слово.")
        if (not (lexdata.slovar.get(lexdata.lemmatizator.get(slovo)) is None) and not (
                lexdata.slovar.get(lexdata.lemmatizator.get(dublslovo)) is None)):
            result = lexdata.wv.distance(w1=str(lexdata.lemmatizator.get(slovo)), w2=str(lexdata.lemmatizator.get(dublslovo)))
            page2_lineText_TextData.delete(1.0, END)
            strD1 = "Расстояние между словами  \n"
            strD2 = str(lexdata.lemmatizator.get(slovo)) + " \n"
            strD3 = str(lexdata.lemmatizator.get(dublslovo)) + " \n"
            strD4 = " = " + str(result)
            page2_lineText_TextData.insert(INSERT, strD1 + strD2 + strD3 + strD4)


######################################################################
# page3  Контекстный анализ предложений


def page3_click_btn_Kontext():
    slugSpis1 = []
    slugSpis2 = []
    slugSpis3 = []
    result = ""
    slovos = []
    # лишнее слово
    predl = page3_lineText_IshPredl.get('1.0', END + '-1c')  #
    predl = predl.strip()
    print(predl)
    predl = wp.tocenizator(predl,lexdata.slovoStop, lexdata.rullmas)
    print(predl)
    result = wp.lemmatizatorPred(predl,lexdata.lemmatizator)
    print(result)
    slovos = result.strip().split(" ")
    slugSpis2.clear()
    print(slovos)
    for slovo in slovos:
        if lexdata.slovar.get(slovo.strip()) is None:
            messagebox.showinfo("Слова " + slovo + " нет в словаре корпуса.", "Введите другое слово.")
            break
        else:
            slugSpis2.append(slovo)
    if len(slugSpis2) == len(slovos):
        for slovo in slugSpis2:
            slugSpis3.append(slovo[0])
        result = wv.doesnt_match(slovos)
        page3_lineText_TextData.delete(1.0, END)
        strD1 = "Лишнее слово в предложении - "
        page3_lineText_TextData.insert(INSERT, strD1 + result)


import operator


# Ищем похожие тизеры
def page3_click_btn_SearchTiz():
        predl1 = page3_lineText_IshPredl.get('1.0', END + '-1c')
        slugSpis1 = []
        slugSpis2 = []
        slugSpis3 = []
        slugSpis4 = []
        # расстояние между фразами

        predl1 = wp.tocenizator(predl1,lexdata.slovoStop, lexdata.rullmas)
        predl1 = wp.lemmatizatorPred(predl1,lexdata.lemmatizator)
        slovos1 = predl1.strip().split()
        k1 = 0
        for slovo in slovos1:
            slovo.strip()
        # обрабатываем предложение 1
        for slovo in slovos1:
            if lexdata.slovar.get(slovo.strip()) is None:
                messagebox.showinfo("Слова " + slovo + " нет в словаре корпуса.", "Введите другое слово.")
                k1 = 1
        slovos2 = ""
        page3_lineText_TextData.delete(1.0, END)
        # print(AllTizer)
        if (k1 == 0):
            iind = 0
            for tizer in lexdata.AllTizer:
                slovos2 = tizer[1].strip().split()
                # print(slovos2)
                result1 = lexdata.wv.wmdistance(slovos1, slovos2)
                # page3_lineText_TextData.delete(1.0,END)
                slugSpis1.append([])
                slugSpis1[iind].append(iind)
                slugSpis1[iind].append(result1)
                iind += 1
            slugSpis1.sort(key=operator.itemgetter(1), reverse=FALSE)
            iind = 0
            for kk in slugSpis1:
                if iind < 4:
                    strD1 = lexdata.AllTizer[kk[0]][0]
                    result1 = kk[1]
                    page3_lineText_TextData.insert(INSERT, strD1 + "{:.4f}".format(result1) + "\n")
                    iind += 1
                else:
                    break


#   Расчет близости фраз по среднему расстоянию между словами
def page3_click_btn_SearchTiz1():
        predl1 = page3_lineText_IshPredl.get('1.0', END + '-1c')
        slugSpis1 = []
        slugSpis2 = []
        slugSpis3 = []
        slugSpis4 = []
        # расстояние между фразами

        predl1 = lexdata.tocenizator(predl1,lexdata.slovoStop, lexdata.rullmas)
        predl1 = lexdata.lemmatizatorPred(predl1,lexdata.lemmatizator)
        slovos1 = predl1.strip().split()
        k1 = 0
        for slovo in slovos1:
            slovo.strip()
        # обрабатываем предложение 1
        for slovo in slovos1:
            if lexdata.slovar.get(slovo.strip()) is None:
                messagebox.showinfo("Слова " + slovo + " нет в словаре корпуса.", "Введите другое слово.")
                k1 = 1
        slovos2 = ""
        kolslov = 0
        wesTiz = 0.0
        page3_lineText_TextData.delete(1.0, END)
        # print(AllTizer)
        if (k1 == 0):
            iind = 0
            for tizer in lexdata.AllTizer:
                slovos2 = tizer[1].strip().split()
                kolslov = 0
                wesTiz = 0.0
                for slovoTitle in slovos1:
                    if lexdata.slovar.get(slovoTitle.strip()):
                        for lexdata.slovoTizer in slovos2:
                            if lexdata.slovar.get(slovoTizer.strip()):
                                kolslov = kolslov + 1
                                # print(slovoTitle,slovoTizer)
                                # print(wv.distance(w1=slovoTitle,w2=slovoTizer))
                                wesTiz = wesTiz + lexdata.wv.distance(w1=slovoTitle, w2=slovoTizer)
                                # print(wesTiz)
                                # print(kolslov)
                result1 = wesTiz / kolslov
                # page3_lineText_TextData.delete(1.0,END)
                slugSpis1.append([])
                slugSpis1[iind].append(iind)
                slugSpis1[iind].append(result1)
                iind += 1
            slugSpis1.sort(key=operator.itemgetter(1), reverse=FALSE)
            iind = 0
            for kk in slugSpis1:
                if iind < 4:
                    strD1 = lexdata.AllTizer[kk[0]][0]
                    result1 = kk[1]
                    page3_lineText_TextData.insert(INSERT, strD1 + "{:.4f}".format(result1) + "\n")
                    iind += 1
                else:
                    break


#   Расчет близости фраз по среднему расстоянию между 3 словами с наименьшим расстоянием
def page3_click_btn_SearchTiz2():
        predl1 = page3_lineText_IshPredl.get('1.0', END + '-1c')
        slugSpis1 = []

        # расстояние между фразами
        predl2 = wp.tocenizator(predl1,lexdata.slovoStop, lexdata.rullmas)
        predl1 = wp.lemmatizatorPred(predl2,lexdata.lemmatizator)
        slovos1 = predl1.strip().split()
        result1 = 0.0
        k1 = 0
        for slovo in slovos1:
            slovo.strip()
        # обрабатываем предложение 1
        for slovo in slovos1:
            if lexdata.slovar.get(slovo.strip()) is None:
                messagebox.showinfo("Слова " + slovo + " нет в словаре корпуса.", "Введите другое слово.")
                k1 = 1
        slovos2 = ""
        wesTiz = []
        page3_lineText_TextData.delete(1.0, END)
        if (k1 == 0):
            iind = 0
            for tizer in lexdata.AllTizer:
                slovos2 = tizer[1].strip().split()
                wesTiz.clear()
                for slovoTitle in slovos1:
                    if lexdata.slovar.get(slovoTitle.strip()):
                        for slovoTizer in slovos2:
                            if lexdata.slovar.get(slovoTizer.strip()):
                                wesTiz.append(lexdata.wv.distance(w1=slovoTitle, w2=slovoTizer))
                wesTiz = sorted(wesTiz)
                if len(wesTiz) > 2: result1 = (wesTiz[0] + wesTiz[1] + wesTiz[2]) / 3
                if len(wesTiz) == 2: result1 = (wesTiz[0] + wesTiz[1]) / 2
                if len(wesTiz) == 1: result1 = wesTiz[0]
                slugSpis1.append([])
                slugSpis1[iind].append(iind)
                slugSpis1[iind].append(result1)
                iind += 1
            slugSpis1.sort(key=operator.itemgetter(1), reverse=FALSE)
            iind = 0
            for kk in slugSpis1:
                if iind < 4:
                    strD1 = lexdata.AllTizer[kk[0]][0]
                    result1 = kk[1]
                    page3_lineText_TextData.insert(INSERT, strD1 + "{:.4f}".format(result1) + "\n")
                    iind += 1
                else:
                    break


#   Расчет близости фраз по среднему расстоянию между словами с расстоянием меньшим середины значений
def page3_click_btn_SearchTiz3():
        predl1 = page3_lineText_IshPredl.get('1.0', END + '-1c')
        slugSpis1 = []

        # расстояние между фразами
        predl2 = wp.tocenizator(predl1,lexdata.slovoStop, lexdata.rullmas)
        predl1 = wp.lemmatizatorPred(predl2,lexdata.lemmatizator)
        slovos1ist = predl1.strip().split()  # Список слов в тайтле
        result1 = 0.0
        k1 = 0
        # обрабатываем предложение 1
        for slovo in slovos1ist:
            if lexdata.slovar.get(slovo.strip()):
                k1 = 1
                break
        slovos2 = ""
        sered = 0.0
        wesTiz = []
        kolvotiz = 0  # количество отбранных тизеров
        page3_lineText_TextData.delete(1.0, END)
        if (k1 == 1):  # В предложении есть слова с которыми можно работать
            iind = 0
            for tizer in lexdata.AllTizer:  # Цикл по всем тизерам
                slovos2 = tizer[1].strip().split()  # разбиваем тизер по словам
                wesTiz.clear()
                for slovoTitle in slovos1ist:  # цикл по словам в тайтлах
                    if lexdata.slovar.get(slovoTitle.strip()):  # Получаем слово тайтла из словаря
                        for slovoTizer in slovos2:  # цикл по всем словам тизера
                            if lexdata.slovar.get(slovoTizer.strip()):  # получаем слово тизера
                                wesTiz.append(wp.wv.distance(w1=slovoTitle,
                                                          w2=slovoTizer))  # ищем расстояние между словом тизера и тайтла
                wesTiz = sorted(wesTiz)
                if len(wesTiz) > 3:
                    sered = wesTiz[0] + (wesTiz[len(wesTiz) - 1] - wesTiz[0]) / 2
                kolvotiz = 0
                result1 = 0.0
                if len(wesTiz) > 3:
                    for ww in wesTiz:
                        if kolvotiz <= len(wesTiz) % 2:
                            result1 = result1 + ww
                            kolvotiz = kolvotiz + 1
                if kolvotiz > 3: result1 = result1 / kolvotiz
                if len(wesTiz) == 3: result1 = (wesTiz[0] + wesTiz[1] + wesTiz[2]) / 3
                if len(wesTiz) == 2: result1 = (wesTiz[0] + wesTiz[1]) / 2
                if len(wesTiz) == 1: result1 = wesTiz[0]
                slugSpis1.append([])
                slugSpis1[iind].append(iind)
                slugSpis1[iind].append(result1)
                iind += 1
            slugSpis1.sort(key=operator.itemgetter(1), reverse=FALSE)
            iind = 0
            for kk in slugSpis1:
                if iind < 4:
                    strD1 = lexdata.AllTizer[kk[0]][0]
                    result1 = kk[1]
                    page3_lineText_TextData.insert(INSERT, strD1 + "{:.4f}".format(result1) + "\n")
                    iind += 1
                else:
                    break
        else:
            page3_lineText_TextData.insert(INSERT, "Подобрать ничего не могу \n")


# Определить пошожесть фраз
def page3_click_btn_Ras():
    # расстояние между фразами
    predl1 = page3_lineText_IshPredl.get('1.0', END + '-1c')
    predl2 = page3_lineText_DublPredl.get('1.0', END + '-1c')
    predl1 = wp.tocenizator(predl1,lexdata.slovoStop, lexdata.rullmas)
    predl1 = wp.lemmatizatorPred(predl1,lexdata.lemmatizator)
    predl2 = wp.tocenizator(predl2,lexdata.slovoStop, lexdata.rullmas)
    predl2 = wp.lemmatizatorPred(predl2,lexdata.lemmatizator)
    slovos1 = predl1.strip().split()
    k1 = 0
    for slovo in slovos1:
        slovo.strip()
    # обрабатываем предложение 1
    for slovo in slovos1:
        if lexdata.slovar.get(slovo.strip()) is None:
            messagebox.showinfo("Слова " + slovo + " нет в словаре корпуса.", "Введите другое слово.")
            k1 = 1

    # обрабатываем предложение 2
    slovos2 = predl2.strip().split()
    k2 = 0
    for slovo in slovos2:
        if lexdata.slovar.get(slovo) is None:
            messagebox.showinfo("Слова " + slovo + " нет в словаре корпуса.", "Введите другое слово.")
            k2 = 1
    if (k1 == 0 and k2 == 0):
        result1 = lexdata.wv.wmdistance(slovos1, slovos2)
        page3_lineText_TextData.delete(1.0, END)
        strD1 = "Расстояние между фразами - "
        page3_lineText_TextData.insert(INSERT, strD1 + "{:.4f}".format(result1))


############################################################################

# page4 Кластеризация по темам


if __name__ == "__main__":
    lexdata=wp.wordprocessing #массив лексических данных
    lexdata.rullmas=wp.rulls()
    root = Tk()
    root.title("Контекстный анализ слов и коротких фраз")
    root.geometry("1200x500")
    mainmenu = Menu(root)
    root.config(menu=mainmenu)
    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label="Открыть...")
    filemenu.add_command(label="Новый")
    filemenu.add_command(label="Сохранить...")
    filemenu.add_command(label="Выход")

    helpmenu = Menu(mainmenu, tearoff=0)
    helpmenu.add_command(label="Помощь")
    helpmenu.add_command(label="О программе")

    mainmenu.add_cascade(label="Файл", menu=filemenu)
    mainmenu.add_cascade(label="Справка", menu=helpmenu)

    Osn = ttk.Notebook()
    page1 = Frame(Osn)
    page2 = Frame(Osn)
    page3 = Frame(Osn)
    Osn.add(page1, text='  Начальные установки  ')
    Osn.add(page2, text='  Контекстный анализ слов  ')
    Osn.add(page3, text='  Контекстный анализ коротких фраз  ')
    Osn.pack(padx=2, pady=3, fill=BOTH, expand=1)

    # page1 Начальные установки
    widthLabe = 500
    widthBt = 300
    heighY = 100
    page1_lineTextFileSlovar = Text(page1)
    page1_lineTextFileSlovar.place(x=10, y=heighY, anchor="w", heigh=30, width=widthLabe, bordermode=OUTSIDE)

    page1_btn_Slovar = Button(page1, text="Выберите файл словаря", command=page1_click_btn_Slovar)
    page1_btn_Slovar.place(x=widthLabe + 15, y=heighY, anchor="w", heigh=30, width=widthBt, bordermode=OUTSIDE)

    page1_lineTextFileVector = Text(page1)
    page1_lineTextFileVector.place(x=10, y=heighY + 50, anchor="w", heigh=30, width=widthLabe, bordermode=OUTSIDE)

    page1_btn_Vector = Button(page1, text="Выберите файл вектора", command=page1_click_btn_Vector)
    page1_btn_Vector.place(x=widthLabe + 15, y=heighY + 50, anchor="w", heigh=30, width=widthBt, bordermode=OUTSIDE)

    page1_lineTextFileLemat = Text(page1)
    page1_lineTextFileLemat.place(x=10, y=heighY + 100, anchor="w", heigh=30, width=widthLabe, bordermode=OUTSIDE)

    page1_clic_btn_Lemmatisator = Button(page1, text="Выберите файл лемматизатора", command=page1_clic_btn_Lemmatisator)
    page1_clic_btn_Lemmatisator.place(x=widthLabe + 15, y=heighY + 100, anchor="w", heigh=30, width=widthBt,
                                      bordermode=OUTSIDE)

    page1_lineTextStop = Text(page1)
    page1_lineTextStop.place(x=10, y=heighY + 150, anchor="w", heigh=30, width=widthLabe, bordermode=OUTSIDE)

    page1_clic_btn_Stop = Button(page1, text="Выберите файл стоп слов", command=page1_clic_btn_Stop)
    page1_clic_btn_Stop.place(x=widthLabe + 15, y=heighY + 150, anchor="w", heigh=30, width=widthBt, bordermode=OUTSIDE)

    page1_lineTextTizer = Text(page1)
    page1_lineTextTizer.place(x=10, y=heighY + 200, anchor="w", heigh=30, width=widthLabe, bordermode=OUTSIDE)

    page1_clic_btn_Tizer = Button(page1, text="Выберите файл тизеров", command=page1_clic_btn_Tizer)
    page1_clic_btn_Tizer.place(x=widthLabe + 15, y=heighY + 200, anchor="w", heigh=30, width=widthBt,
                               bordermode=OUTSIDE)

    # page2 Контекстный анализ слов
    page2_lineText_KolSlovo = Text(page2)
    page2_lineText_KolSlovo.place(x=10, y=heighY - 50, anchor="w", heigh=30, width=35, bordermode=OUTSIDE)
    page2_lineText_KolSlovo.insert(1.0, "20")

    page2_lineText_Porog = Text(page2)
    page2_lineText_Porog.place(x=10, y=heighY - 80, anchor="w", heigh=30, width=35, bordermode=OUTSIDE)
    page2_lineText_Porog.insert(1.0, "100")

    page2_label_Kol_Slovo = Label(page2, text="Количество слов в выдаче. По умолчанию 20")
    page2_label_Kol_Slovo.place(x=45, y=heighY - 50, anchor="w", heigh=30, width=350, bordermode=OUTSIDE)

    page2_label_Porog = Label(page2, text="Отсечка слов по частоте. По умолчанию 100")
    page2_label_Porog.place(x=45, y=heighY - 80, anchor="w", heigh=30, width=350, bordermode=OUTSIDE)

    page2_label_Nom1_Slovo = Label(page2, text="Слово 1")
    page2_label_Nom1_Slovo.place(x=20, y=heighY - 20, anchor="w", heigh=20, width=100, bordermode=OUTSIDE)

    page2_lineText_IshSlovo = Text(page2)
    page2_lineText_IshSlovo.place(x=10, y=heighY, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    page2_btn_Kontext = Button(page2, text="Показать контекст слова", command=page2_click_btn_Kontext)
    page2_btn_Kontext.place(x=215, y=heighY, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    page2_label_Nom2_Slovo = Label(page2, text="Слово 2")
    page2_label_Nom2_Slovo.place(x=20, y=heighY + 30, anchor="w", heigh=20, width=100, bordermode=OUTSIDE)

    page2_lineText_DublSlovo = Text(page2)
    page2_lineText_DublSlovo.place(x=10, y=heighY + 50, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    page2_btn_Ras = Button(page2, text="Рассчитать расстояние между словами", command=page2_click_btn_Ras)
    page2_btn_Ras.place(x=10, y=heighY + 100, anchor="w", heigh=30, width=300, bordermode=OUTSIDE)

    page2_lineText_TextData = Text(page2)
    page2_lineText_TextData.place(x=450, y=heighY - 90, anchor="nw", heigh=360, width=500, bordermode=OUTSIDE)

    # page3 Контекстный анализ предложений

    # Ввод первого предложения
    page3_label_Nom1_Predl = Label(page3, text="Предложение 1")
    page3_label_Nom1_Predl.place(x=20, y=heighY - 70, anchor="w", heigh=20, width=120, bordermode=OUTSIDE)

    page3_lineText_IshPredl = Text(page3)
    page3_lineText_IshPredl.place(x=10, y=heighY - 30, anchor="w", heigh=60, width=400, bordermode=OUTSIDE)

    page3_btn_Kontext = Button(page3, text="Показать лишнее слово", command=page3_click_btn_Kontext)
    page3_btn_Kontext.place(x=415, y=heighY - 46, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    page3_btn_SearchTiz = Button(page3, text="Подходящие тизеры V1", command=page3_click_btn_SearchTiz)
    page3_btn_SearchTiz.place(x=415, y=heighY - 14, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    page3_btn_SearchTiz1 = Button(page3, text="Подходящие тизеры V2", command=page3_click_btn_SearchTiz1)
    page3_btn_SearchTiz1.place(x=415, y=heighY + 16, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    page3_btn_SearchTiz2 = Button(page3, text="Подходящие тизеры V3", command=page3_click_btn_SearchTiz2)
    page3_btn_SearchTiz2.place(x=415, y=heighY + 46, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    page3_btn_SearchTiz3 = Button(page3, text="Подходящие тизеры V4", command=page3_click_btn_SearchTiz3)
    page3_btn_SearchTiz3.place(x=415, y=heighY + 76, anchor="w", heigh=30, width=200, bordermode=OUTSIDE)

    # Ввод второго предложения
    page3_label_Nom2_Predl = Label(page3, text="Предложение 2")
    page3_label_Nom2_Predl.place(x=20, y=heighY + 40, anchor="w", heigh=20, width=120, bordermode=OUTSIDE)

    page3_lineText_DublPredl = Text(page3)
    page3_lineText_DublPredl.place(x=10, y=heighY + 80, anchor="w", heigh=60, width=400, bordermode=OUTSIDE)

    page3_btn_Ras = Button(page3, text="Рассчитать расстояние между предложениями", command=page3_click_btn_Ras)
    page3_btn_Ras.place(x=10, y=heighY + 130, anchor="w", heigh=30, width=400, bordermode=OUTSIDE)

    # Поле вывода результата
    page3_lineText_TextData = Text(page3)
    page3_lineText_TextData.place(x=620, y=heighY - 90, anchor="nw", heigh=450, width=550, bordermode=OUTSIDE)

root.mainloop()