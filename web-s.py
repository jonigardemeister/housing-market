#!/usr/bin/python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd

df_cities = pd.read_csv('cities.csv', encoding='utf-8')
row_list = list()
columns = ['Kaupunginosa','Huoneisto','Talot','m2','hinta','e/m2','Rakennusvuosi','Kerros','Hissi','Kunto','Tontti','Energialuokka','Kunta']

driver = webdriver.Chrome("/Library/Frameworks/Python.framework/Versions/3.9/bin/chromedriver")

for city in df_cities['Kunta']:
    print(city)
    driver.get("https://asuntojen.hintatiedot.fi/haku/?c="+city+"&cr=1&ps=&nc=0&amin=&amax=&renderType=renderTypeTable&search=1")

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    index = 0

    while(soup.find('input',{'class': 'submit', 'value':'seuraava sivu »'}) and index < 100):
        table = soup.find('table', {"id": "mainTable"})
        rows = table.find_all('tr')

        for tr in rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            if(len(row) == 12):
                row_list.append(row)

        try:
            button = driver.find_element_by_xpath("//input[@value='seuraava sivu »']")
            picture = button.click()
        except NoSuchElementException:
            break

        df = pd.DataFrame(row_list, columns=columns)
        print(df.shape)
        df.to_csv('beautifulsoup.csv', index=False, encoding='utf-8-sig')
        index += 1

df = pd.DataFrame(row_list,columns=columns)
df.dropna(subset=columns, inplace=True)
df.to_csv('beautifulsoup.csv', index=False, encoding='utf-8-sig')
