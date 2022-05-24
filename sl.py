from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

import json
import pandas as pd


df = pd.read_csv('Amazon Scraping - Sheet1.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
Asin = df['Asin']
country = df['country']
d = {}
na = []

for i in range(len(df)):
    url = 'https://www.amazon.{}/dp/{}'.format(country[i], Asin[i])
    driver = webdriver.Chrome("chromedriver.exe")
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    #driver.refresh()
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'html.parser')
    
    #print('done')
    
    try:
        title = soup.find("span", {"id": "productTitle"}).get_text()
        title = title.strip()
        
        img = soup.find("img", {"id": "imgBlkFront"}).get('src')
        
        ul = soup.find("ul", {"class": "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"})
        data = ul.find_all("li")
        li = []
        for item in data:
            s = ""
            for ele in item.text.split():
                if ele=='\u200f' or ele=='\u200e':
                    continue
                s = s + ele + ' '
            li.append(s.strip())
        
        try:
            price = soup.find("span", {"id": "price"}).get_text()
            price = price.strip()
            print("{} m1) TITLE :{} | PRICE :{} | IMG :{}".format(i, title, price, img))
            d[i] = {'title': title, 'price': price, 'img': img, 'details': li}
        
        except:
            try:
                a = soup.find("span", {"class": "a-size-base a-color-price a-color-price"}).get_text()
                price = a.strip()
                print("{} m1) TITLE :{} | PRICE :{} | IMG :{}".format(i, title, price, img))
                d[i] = {'title': title, 'price': price, 'img': img, 'details': li}
            
            except:
                try:
                    a = soup.find_all("span", {"class": "a-color-base"})
                    price = a[1].get_text().strip()
                    print("{} m1) TITLE :{} | PRICE :{} | IMG :{}".format(i, title, price, img))
                    d[i] = {'title': title, 'price': price, 'img': img, 'details': li}
                    
                except:
                    try:
                        price = soup.find("span", {"class": "a-offscreen"}).get_text()
                        price = price.strip()
                        print("{} m1) TITLE :{} | PRICE :{} | IMG :{}".format(i, title, price, img))
                        d[i] = {'title': title, 'price': price, 'img': img, 'details': li}
                    
                    except:
                        print("{}) NOT AVAILABLE | {}".format(i, url))
                        na.append(url)
    except:
        print("{}) NOT AVAILABLE | {}".format(i, url))
        na.append(url)
    
    if len(d) == 110:
        break

jsonDump = open("res.json", "w")
jsonDump.write(json.dumps(d))
jsonDump.close()