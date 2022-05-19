from fake_useragent import UserAgent
from config import proxies_file
import requests
from random import choice
import gc

ua = UserAgent()
proxies = open(proxies_file).read().split('\n')

def get_html(url, params=None):
    useragent = {'User-Agent': ua.random}
    proxy = {'http': 'http://' + choice(proxies)}
    r = requests.get(url.strip(), params=params, headers=useragent, proxies=proxy)
    del useragent, proxy
    gc.collect()
    return r.text