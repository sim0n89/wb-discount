import proxies
import db
import categories
from config import potok
from multiprocessing import Pool
from products import get_products_from_category


def main():
    proxies.main()
    db.clear_root()
    category_links = categories.get_category_links()
    with Pool(potok) as p:
        p.map(get_products_from_category, category_links)

if __name__ == '__main__':
    while True:
         main()
