import requests
import json
from config import except_men_items
import gc

def get_categories(url):
    r = requests.get(url)
    return (r.text)


def get_category_links():
    menu = get_categories('https://www.wildberries.ru/gettopmenuinner?lang=ru')
    json_menu = json.loads(menu)
    arr_menu = json_menu['value']['menu']
    links = []
    for menu_item in arr_menu:
        if menu_item['id'] in except_men_items:
            for child in menu_item['childs']:
                links.append(child['pageUrl'])
    del json_menu, arr_menu
    gc.collect()
    return links