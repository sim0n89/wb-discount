# coding=utf-8
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
import gc
ua = UserAgent()
proxies = open(proxies_file).read().split('\n')
gc.collect()

logging.basicConfig(
    level=logging.WARNING,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)


def get_products_from_category(url):
    category_url = HOST + url + '?sort=sale'
    session = HTMLSession()
    session.headers = {'User-Agent': ua.random}
    session.proxies = {'http': 'http://' + choice(proxies)}
    r = session.get(category_url)
    r.html.render(sleep=3)
    r.close()
    session.close()
    try:
        prod_count = int("".join(filter(str.isdecimal, r.html.find('.goods-count', first=True).text)))
    except:
        prod_count = 200
    page_count = math.ceil(prod_count / 100)
    if page_count > 100:
        page_count = 100
    cards = []
    for i in range(1, int(page_count/2)):
        url = category_url + '&page=' + str(i)
        cards = []
        session = HTMLSession()
        session.headers = {'User-Agent': ua.random}
        session.proxies = {'http': 'http://' + choice(proxies)}
        r = session.get(url)
        try:
            r.html.render(sleep=3)
            r.close()
            session.close()
            try:
                cards = r.html.find('.catalog-page__content .product-card')
            except:
                cards = []

            if len(cards) > 0:
                # list(map(check_product, cards))
                for card in cards:
                    check_product(card)
            del cards, r, session
            gc.collect()
        except:
            del cards, r, session
            continue
    del page_count, prod_count
    gc.collect()





def check_product(card):
    prID = 0
    price = 0
    try:
        if 'product-card--fake' not in card.attrs['class']:
            prID = int("".join(filter(str.isdecimal, card.find('a', first=True).attrs['href'])))
            price = int("".join(filter(str.isdecimal, card.find('.lower-price', first=True).text)))
    except Exception:
        traceback.print_exc()
    if prID != 0 or price != 0:
        check = db.check_product(prID)
        if check == False:
            db.new_product(prID, price)
        else:
            try:
                dbID = check[0][0]
                prices = db.get_prices(dbID)
                last_price = prices[-1][2]

                if int(price) <= int(last_price) * 0.6:
                    try:
                        prod = product.get_product_info(prID)
                        print(prod)
                        have_root = db.check_root(prod['root'])
                        if have_root:
                            db.add_root(prod['root'])
                            prod['last_price'] = last_price
                            prod['prices'] = prices
                            message.send_product_message(prod)
                            db.add_new_price(dbID, price)
                            del dbID, price, prod, last_price, prices, have_root
                            gc.collect()
                    except Exception:
                        traceback.print_exc()

                elif price > int(last_price):
                    db.add_new_price(dbID, price)
                    del dbID, price, last_price

                else:
                    pass

            except Exception:
                traceback.print_exc()
            del check
    gc.collect()


if __name__ == '__main__':
    get_products_from_category('/catalog/detyam/dlya-devochek')


