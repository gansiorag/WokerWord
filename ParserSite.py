'''
Created on 14 дек. 2018 г.

@author: al
'''

import sys
from html.parser import HTMLParser
import re
#import requests
from urllib.request import urlopen
import sqlite3

class MyHTMLParser(HTMLParser):
    def __init__(self, site_name,  bazaName, fileName, site_nameZn,*args, **kwargs):
        # список ссылок
        self.links = []
        # имя сайта
        self.site_name = site_name
        self.site_nameZn = site_nameZn
        self.fileName=fileName
        self.bazaName= bazaName
        # вызываем __init__ родителя
        super().__init__(*args, **kwargs)
        # при инициализации "скармливаем" парсеру содержимое страницы
        self.feed(self.read_site_content())
        # записываем список ссылок в файл
        self.write_to_baza()
        
        
    def handle_starttag(self, tag, attrs):
     # проверяем является ли тэг тэгом ссылки
        if tag == 'a':
         # находим аттрибут адреса ссылки
         for attr in attrs:
           if attr[0] == 'href':
                 # проверяем эту ссылку методом validate() (мы его еще напишем)
                 if not self.validate(attr[0]):
                     # вставляем адрес в список ссылок
                        if not self.site_name in attr[1]:
                             self.links.append(attr[1])
                          
    def validate(self, link):
      return (link in self.links) or ('#' in link) or ('javascript:' in link)
      """ 
        Функция проверяет стоит ли добавлять ссылку в список адресов. 
          В список адресов стоит добавлять если ссылка:
          1) Еще не в списке ссылок
          2) Не вызывает javascript-код
          3) Не ведет к какой-либо метке. (Не содержит #) 
      """
    def read_site_content(self):
      print ("Загрузка сайта", file=sys.stderr)
      #r =  requests.get(self.site_name)
      r = urlopen(self.site_name).read()
      print ("сайт загружен", file=sys.stderr)
      print (str(r), file=sys.stderr)
      return str(r)     
  
    def write_to_baza(self):
         BazaAnaliz = sqlite3.connect(self.bazaName)
         cursor = BazaAnaliz.cursor()
         print(self.links[:30], file=sys.stderr)
         for spis_links in self.links:
           cursor.execute("INSERT INTO silki (silkizn) VALUES (?)",(spis_links,))
           print(spis_links, file=sys.stderr)
         BazaAnaliz.commit()
         BazaAnaliz.close()
         print("The End;", file=sys.stderr)  
        
           
    def write_to_file(self):    
     # открываем файл
      f = open(self.fileName, 'a')
     # записываем отсортированный список ссылок, каждая с новой строки
      f.write('\n'.join(sorted(self.links)))
     # закрываем файл
      f.close()                     
                                 


def parserSite( AdresSite,FileBaza,FileModel,AdresSiteZn):
      parser = MyHTMLParser(AdresSite,FileBaza,FileModel,AdresSiteZn)
  
  
  
  
    