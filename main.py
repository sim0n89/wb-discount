import proxies
import db
import logging
import categories
from config import potok
from multiprocessing import Pool
from products import get_products_from_category
import gc


logging.basicConfig(
    level=logging.WARNING,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)


def main():
    while True:
        proxies.main()
        db.clear_root()
        category_links = categories.get_category_links()
        with Pool(potok) as p:
            p.map(get_products_from_category, category_links)
        # for category in category_links:
        #     get_products_from_category(category)
        del category_links
        gc.collect()


if __name__ == '__main__':
    while True:
        main()
