from requests_html import HTMLSession
from fake_useragent import UserAgent
from config import proxies_file
from random import choice
from config import HOST
import get_html
import json
import math

ua = UserAgent()
proxies = open(proxies_file).read().split('\n')

def get_price_history(id):
    url = 'https://wbx-content-v2.wbstatic.net/price-history/'+str(id)+'.json'
    try:
        price_history = get_html.get_html(url)
    except:
        price_history=''
    return price_history


def get_stock(id):
    url = f'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043&appType=1&locale=ru&lang=ru&curr=rub&dest=-1029256,-102269,-1278703,-1255563&nm={id}'
    st = {}
    try:
        html = get_html.get_html(url)
        s = json.loads(html)
        root = s['data']['products'][0]['root']
        sizes = s['data']['products'][0]['sizes']

        stock= 0
        for size in sizes:
            if len(size['stocks'])>0:
                for wh in size['stocks']:
                    stock = stock + wh['qty']
        st['stock'] = stock
        st['root'] = root
    except:
        st['stock'] = ''
        st['root'] = ''
    return st


def get_product_info(id):
    url = f'https://www.wildberries.ru/catalog/{id}/detail.aspx?targetUrl=GP'
    price_history = get_price_history(id)
    stock = get_stock(id)
    if price_history != '':
        parse = json.loads(price_history)
        lenth_list = len(parse)
        price_list = []
        for n in range(lenth_list):
            price_list.append(math.ceil(parse[n]['price']['RUB']/100))
        try:
            maxmimum = max(price_list)
        except:
            maxmimum = 0
            minimum = 0
        try:
            minimum = min(price_list)
        except:
            minimum = 0
    else:
        maxmimum = 0
        minimum = 0

    session = HTMLSession()
    session.headers = {'User-Agent': ua.random}
    session.proxies = {'http': 'http://' + choice(proxies)}
    r = session.get(url)

    try:
        name = r.html.find('h1.same-part-kt__header', first=True).text.strip()
    except:
        name=''

    try:
        image = r.html.find('.photo-zoom__preview', first=True).attrs['src']
    except:
        image = ''

    try:
        price = r.html.find('.price-block__final-price', first=True).text.strip()
        price = int("".join(filter(str.isdecimal, price)))
    except:
        price = 0

    try:
        old_price = r.html.find('.price-block__old-price', first=True).text.strip()
        old_price = int("".join(filter(str.isdecimal, old_price)))
    except:
        old_price = 0

    if price < minimum:
        price_text = 'цена ниже диапозона'
        smile = '📉'
    elif price > maxmimum:
        price_text = 'цена выше диапозона'
        smile = '📈'
    elif price < maxmimum and price > minimum:
        price_text = 'Цена в диапазоне'
        smile = '📊'
    if price_history == '':
        price_text = 'Цена без диапазона'
        smile = '🤑'

    product = {
        "name": name,
        "price": price,
        "old_price": old_price,
        "url": url.replace('?targetUrl=GP', ''),
        "image": "https:" + image,
        "smile": smile,
        'stock': stock['stock'],
        'root': stock['root'],
        "price_min": minimum,
        "price_max": maxmimum,
        "price_text": price_text,
    }


    try:
        discound = math.ceil((price/old_price)*100 - 100)
        product["discount"] = discound

    except:
        product["discount"] = 0
    print(product)
    return product

if __name__ == '__main__':
    get_product_info('78823134')
