from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import sqlite3 as sql
import random
import os
import re


class Wallpaper():
    def __init__(self):
        self.allAphorism_db = sql.connect("allAphorism") # Veri Tabanı Oluşturuldu
        self.cursor = self.allAphorism_db.cursor() #İmleç Oluşturuldu
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ozlu_sozler (soz)") #Özlü Sözler tablosu oluşturuldu.


    def addAphorism(self,number):
        headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"} # Websitelerine kendimizi tarayıcı gibi tanıttık.
        site_link = "https://evrimagaci.org/sozler" # Gireceğimiz sitenin linkini verdik.
        r = requests.get(site_link, headers=headersparam) # Siteye istek attık.
        soup = bs(r.content, "lxml", from_encoding='UTF-8') # Siteyi parselledik.

        tag = soup.find_all("div", attrs={"class": "quote-con"}) # Özlü sözlerin olduğu div-i seçtik.
        for i in range(number): # Kullanıcının istediği kadar özlü sözü çekmeye başladık.
            tagContent = tag[i].find("a").text # Div-in içindeki <a> etiketininin contentini aldık.
            self.cursor.execute("INSERT INTO ozlu_sozler VALUES (?)",(tagContent,)) # Contenti (özlü sözü) veri tabanına yerleştirdik.
            self.allAphorism_db.commit() # Veri tabanına güncellemeyi kaydettirdik.




    def changeContent(self):
        
        randomAphorism_get = self.cursor.execute("SELECT * FROM ozlu_sozler ORDER BY RANDOM() LIMIT 1;") # Veritabanından rastgele bir söz seçtik.
        randomAphorism_fetch = self.cursor.fetchall() # Seçtiğimiz sözü nesnelleştirip değişkene kaydettik.
        randomAphorism_str = str(randomAphorism_fetch) # Hataların önüne geçmek için öncelikle çektiğimiz sözü string ifadeye çevirdik.
        randomAphorism_list = list(randomAphorism_str) # Sonra ise istenmeyen kısımları silmek için listeye dönüştürdük.

        for i in range(5):
            randomAphorism_list.pop(0) # Baştaki 5 gereksiz karakteri sildik.

        for x in range(4):
            randomAphorism_list.pop(-1) # Sondaki 4 gereksiz karakteri sildik.

        randomAphorism_new = "" # Listedeki özlü sözümüzü stringe çevirmek için bir boş str yarattık.
        for y in randomAphorism_list:
            randomAphorism_new += y # Listedeki her elemanı stringe yazdık.

        base = os.path.dirname(os.path.abspath(__file__)) # Proje yolu ile ilgili bir komut.
        html = open(os.path.join(base, 'wallpaper.html')) # Html dosyamızı bulduk.
        soup = bs(html, "html.parser")  # Dosyamızı bs4 ile parselledik ve değişkene kaydettik.

        tag = soup.find("span", {"id":"aphorism"}) # HTML dosyasındaki özlü sözümüzün alanını bulduk.
        soup.span.clear()   # Özlü söz alanını temizledik.
        soup.span.append(randomAphorism_new) # Özlü söz alanına, özlü sözümüzü ekledik.


        # tag.find(text=re.compile(tag_text)).replace_with(randomAphorism_new)
        with open("wallpaper.html", "wb") as f_output: 
            f_output.write(soup.prettify("utf-8")) # Değişiklikleri kaydettik.

    def changeBackground(self):
        browser = webdriver.Chrome(executable_path="chromedriver.exe")
        browser.get("https://cloudconvert.com/html-to-jpg")
        browser.maximize_window()
        while 1:
            try:
                htmlfile = "C:\\Users\\isden\\Masaüstü\\WallpaperGenerator\\wallpaper.html"
                fileinput = browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div/div/input')
                fileinput.send_keys(htmlfile)
                time.sleep(3)
                browser.find_element(By.XPATH ,'//*[@id="app"]/div/div[2]/div/div[3]/div[4]/button').click()
                break
            except Exception as e:
                print(f"HATA BUTON \n{e}")

        while 1:
            try:
                link = browser.find_element(By.XPATH ,'//*[@id="__BVID__60___BV_modal_footer_"]/a').href
                browser.get(link)
            except:
                print("HATA İNDİRME")


        

        time.sleep(5)
    

   

object = Wallpaper()
object.changeBackground()


