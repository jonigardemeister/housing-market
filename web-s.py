#!/usr/bin/python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime

def fetch_rows_from_page(soup):
    result = list()

    table = soup.find('table', {"id": "mainTable"})
    rows = table.find_all('tr')

    for tr in rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        row.append(city)
        if(len(row) == 13):
            result.append(row)
            
    return result


now = datetime.now()

now_date = now.strftime("%d_%m_%Y")

df_cities = pd.read_csv('data/cities.csv', encoding='utf-8')
row_list = list()
columns = ['Kaupunginosa','Huoneisto','Talot','m2','hinta','e/m2','Rakennusvuosi','Kerros','Hissi','Kunto','Tontti','Energialuokka','Kunta']

driver = webdriver.Chrome()

for city in df_cities['Kunta']:
    print(city)
    driver.get("https://asuntojen.hintatiedot.fi/haku/?c="+city+"&cr=1&ps=&nc=0&amin=&amax=&renderType=renderTypeTable&search=1")

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    index = 0

    while(soup.find('input',{'class': 'submit', 'value':'seuraava sivu »'}) and index < 100):
        
        row_list.extend(fetch_rows_from_page(soup))

        try:
            button = driver.find_element(By.XPATH, "//input[@value='seuraava sivu »']")
            picture = button.click()
        except NoSuchElementException:
            break

        index += 1

    row_list.extend(fetch_rows_from_page(soup))

df = pd.DataFrame(row_list, columns=columns)
df.dropna(subset=columns, inplace=True)
df.to_csv(f'data/results/data_{now_date}.csv', index=False, encoding='utf-8-sig')
