from asyncio import tasks
from bs4 import BeautifulSoup as bs
import requests
import csv
import re
import os
import asyncio
import json
from time import sleep
import time

scr_urls = ['https://www.ozon.ru/product/hd-televizor-hartens-htv-24hdr06b-24-357682561/',
         'https://www.ozon.ru/product/besprovodnye-naushniki-jbl-reflect-flow-pro-belyy-357032648/?ectx=0&sh=FKs0RzHw']
enum_url = 'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?page='

wFile = open("ozon_res.csv", mode = "w", encoding = 'utf-8')
names = ["Наименование", "Цена со скидкой", "Цена без скидки", "Описание", "Ссылки на картинки", "Имена картинок", "Разделы", "Ссылка на товар"]
file_writer = csv.DictWriter(wFile, delimiter = ';', lineterminator = '\n', fieldnames = names)
file_writer.writeheader()

async def scrap_ozon(good_url):
    header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'
    }

    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, good_url, header)
    response = await future
    bsobj = bs(response.content, 'html.parser')

    try:
        name = bsobj.find('h1', {'class': 'e8j2'}).text
    except:
        name = 'no_data'

    try:
        specifications_1 = bsobj.find_all('dt', {'class': 'db4'})
        specifications_2 = bsobj.find_all('dd', {'class': 'db5'})
        specifications_text = list()
        for i in range(len(specifications_1)):
            specifications_text.append(specifications_1[i].text + ' - ' + specifications_2[i].text)
    except:
        specifications_text.append('no_data')

    try:
        imageurls = bsobj.find_all('div', {'class': 'e9q9'})
        imgs = list()
        image_names = list()

        for imgurl in imageurls:
            imgurl = imgurl.find('img')['src']
            imgs.append(imgurl.replace(imgurl[imgurl.find('/', (imgurl.rfind('/') - 5)):imgurl.rfind('/')], ''))

        try:   
            dirname = ''.join(filter(str.isalnum, name))
            os.mkdir('img/' + dirname)
        except:
            dirname = ''.join(filter(str.isalnum, name))

        for img in imgs:
            image_names.append(img[img.rfind('/')+1:])
            img_data = loop.run_in_executor(None, requests.get, img)
            img_resp = await img_data

            with open('img/'+ dirname + '/' + image_names[len(image_names) - 1], 'wb') as fw:
                fw.write(img_resp.content)
    except:
        imgs.append('no_data')
        image_names.append('no_data')

    try:
        price = " ".join(re.findall('\d+', bsobj.find('span', {'class': 'c2h5'}).text))
    except:
        price = 'no_data'

    try:
        old_price = " ".join(re.findall('\d+', bsobj.find('span', {'class': 'c2h8'}).text))
    except:
        old_price = 'no_data'

    try:
        chapters = bsobj.find_all('li', {'class': 'bd9'})
        chapters_text = str()

        for chapter in chapters:
            chapters_text += chapter.text
    except:
        chapters_text = 'no_data'

    file_writer.writerow({"Наименование": name, "Цена со скидкой": price, "Цена без скидки": old_price,
                          "Описание": specifications_text, "Ссылки на картинки": imgs , "Имена картинок": image_names,
                          "Разделы": chapters_text, "Ссылка на товар": good_url})

async def main(url_list):
    tasks = [asyncio.create_task(scrap_ozon(url)) for url in url_list]
    await asyncio.gather(*tasks)

def get_urls(base_url, i_pages):
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'
            }
    session = requests.Session()

    out_urls = list()
    for i in range(i_pages):
        try:
            cur_url = base_url + str(i+1)
            response = session.get(cur_url, headers=header)
            bsobj = bs(response.content, 'html.parser')
            url_json = bsobj.find('div', {'id': 'state-searchResultsV2-252189-default-1'})
            item_json = json.loads(url_json['data-state'])
            
            for item in item_json['items']:
                out_urls.append('https://www.ozon.ru' + item['action']['link'])
        except:
            print("Sleeping...")
            sleep(3)
            print("Waking...")
            continue

    return out_urls
  

if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(get_urls(enum_url, 31)))
    print("By " + str(time.time() - start_time) + " seconds")
