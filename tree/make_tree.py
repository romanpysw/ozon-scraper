import requests
from time import sleep

category_urls = ['https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=15500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=7500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=17777',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=14500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=7000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=6500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=10500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=11000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=9700',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=9200',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=6000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=12300',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=8500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=33332',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=16500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=15000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=50001',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=13500',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=7697',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=13300',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=18000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=9000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=8000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=32056',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=14572',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=25000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=13100',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=60000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=34452',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=21000',
                'https://www.ozon.ru/api/composer-api.bx/_action/categoryChildV2?menuId=1&categoryId=35659']

def get_category_tree(cat_urls):
    header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'}
    session = requests.Session()
    json_text = '{'

    for url in cat_urls:       
        print('Making GET to: ' + url)
        response = session.get(url, headers=header)
        json_text += '"' + url + '"' + ':' + response.text + ','
        print('Go to sleep')
        sleep(5)

    json_text = json_text[:-1]
    json_text += '}'

    with open('tree.json', 'w', encoding="utf-8") as fw:
        fw.write(json_text)


if __name__ == "__main__":
    get_category_tree(category_urls)