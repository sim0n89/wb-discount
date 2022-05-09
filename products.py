import message
import logging
from requests_html import HTMLSession
from fake_useragent import UserAgent
from config import proxies_file
from random import choice
from config import HOST
import math
import traceback
import db
import product

ua = UserAgent()
proxies = open(proxies_file).read().split('\n')

logging.basicConfig(
    level=logging.DEBUG,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )


def get_products_from_category(url):
    category_url = HOST + url + '?sort=sale'
    session = HTMLSession()
    session.headers = {'User-Agent': ua.random}
    session.proxies = {'http': 'http://' + choice(proxies)}
    r = session.get(category_url)
    r.html.render(sleep=3, keep_page=True)
    try:
        prod_count = int("".join(filter(str.isdecimal, r.html.find('.goods-count', first=True).text)))

    except:
        prod_count = 200

    page_count = math.ceil(prod_count / 100)
    if page_count>100:
        page_count=100
    for i in range(1, int(page_count/2)):
        url = category_url + '&page=' + str(i)
        print(url)
        session.headers = {'User-Agent': ua.random}
        session.proxies = {'http': 'http://' + choice(proxies)}
        r = session.get(url)
        r.html.render(sleep=3, keep_page=True)
        try:
            cards = r.html.find('.catalog-page__content .product-card')
        except:
            cards=[]

        if len(cards)>0:
            list(map(check_product , cards))



def check_product(card):
    prID = 0
    price = 0
    try:

        if 'product-card--fake' not in card.attrs['class']:
            prID = card.find('a', first=True).attrs['href'].replace('/catalog/', '').replace('/detail.aspx?targetUrl=GP', '')
            price = int("".join(filter(str.isdecimal, card.find('.lower-price', first=True).text)))

    except Exception:
        traceback.print_exc()
    if prID!=0 or price!=0:
        check = db.check_product(prID)
        if check == False:
            db.new_product(prID, price)
        else:
            dbID = check[0][0]
            prices = db.get_prices(dbID)
            last_price = prices[-1][2]
            print(price, last_price)
            if int(price) <= int(last_price)*0.7:
                try:
                    prod = product.get_product_info(prID)
                    print(prod)
                    have_root = db.check_root(prod['root'])
                    if have_root:
                        db.add_root(prod['root'])
                        prod['last_price'] = last_price
                        message.send_product_message(prod)
                        db.add_new_price(dbID, price)
                except Exception:
                    traceback.print_exc()

            elif price > int(last_price):
                db.add_new_price(dbID, price)
            else:
                pass



