import requests
from  config import proxies_file

url = 'https://hidemy.name/ru/api/proxylist.php?out=plain&maxtime=500&code=236208136007189'


def take_proxies(url):
    r = requests.get(url)
    return (r.text)


def save_proxi(pr):
    file = open(
        proxies_file, 'w')
    file.write(pr)
    file.close


def main():
    proxies = take_proxies(url)
    save_proxi(proxies)


if __name__ == '__main__':
    main()