from config import TOKEN, channel_id
import telebot
from telebot import types
import traceback

bot = telebot.TeleBot(TOKEN)


def send_message(message):
    try:
        bot.send_message(channel_id, message)
    except Exception:
        traceback.print_exc()



def send_product_message(product):
    # img = open(product['image'], 'rb')
    # bot.send_photo(channel_id,product['image'] ,caption="TEST")
    product_message = make_product_message(product);
    bot.send_photo(channel_id,product['image'], parse_mode="html", caption=product_message)

def make_product_message(product):
    if product['old_price']!=0:
        text_old_price = f'<del>{str(product["old_price"])}₽ </del>'
    else:
        text_old_price=''
    if product['discount']!=0:
        text_discound = '🔥Скидка:' + str(product['discount']) + '%'
    else:
        text_discound = ''
    if product['price_min'] == product['price_max']:
        d_text = ''
    else:
        d_text = f"↔️Диапозон: {str(product['price_min'])}₽ - {str(product['price_max'])}₽\n"

    text = f'''{product['smile']} {str(product['price'])}₽ {text_old_price} 🛍 {product['name']} \n
{text_discound}
Предыдущая цена: {product['last_price']}₽
🤔Остаток: {str(product['stock'])}шт
{d_text}
{product['url']}'''
    return text