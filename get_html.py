from fake_useragent import UserAgent
from config import proxies_file
import requests
from random import choice

ua = UserAgent()
proxies = open(proxies_file).read().split('\n')

def get_html(url, params=None):
    useragent = {'User-Agent': ua.random}
    proxy = {'http': 'http://' + choice(proxies)}
    r = requests.get(url.strip(), params=params, headers=useragent, proxies=proxy)

    return r.text