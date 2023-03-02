import requests
from bs4 import BeautifulSoup as bs
import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')

MINFIN_URL_USD = "https://minfin.com.ua/ua/currency/auction/usd/sell/dnepropetrovsk/?compact=true"
MINFIN_URL_EUR = "https://minfin.com.ua/ua/currency/auction/eur/sell/dnepropetrovsk/?compact=true"

@bot.message_handler(commands=['start'])
def start(message):
    markup = show_keyboard()
    bot.send_message(message.chat.id,
                     text="Привіт, {0.first_name}!".format(message.from_user),
                     reply_markup=markup)

def show_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton("Дізнатися курс")
    markup.add(button_1)
    return markup

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    if message.text == "Дізнатися курс":
        bot.send_message(message.from_user.id, answer_string())

def update_time():
    r = requests.get(MINFIN_URL_USD)
    soup = bs(r.text, "html.parser")
    update_time = soup.find("div", {"class": "Statistics__updated"})
    return(update_time.text)

def get_current_exchange_rate():
    r_usd = requests.get(MINFIN_URL_USD)
    r_eur = requests.get(MINFIN_URL_EUR)

    buy_array = []
    sale_array = []

    soup_usd = bs(r_usd.text, "html.parser")
    buy_source = soup_usd.find("div", {"class": "buy"}).find("span", {"variant": "cardHeadlineL"}, recursive=False)
    sale_source = soup_usd.find("div", {"class": "sale"}).find("span", {"variant": "cardHeadlineL"}, recursive=False)

    for buy_target in buy_source:
        buy_array.append(buy_target.text.strip())
    for sale_target in sale_source:
        sale_array.append(sale_target.text.strip())

    soup_eur = bs(r_eur.text, "html.parser")
    buy_source = soup_eur.find("div", {"class": "buy"}).find("span", {"variant": "cardHeadlineL"}, recursive=False)
    sale_source = soup_eur.find("div", {"class": "sale"}).find("span", {"variant": "cardHeadlineL"}, recursive=False)

    for buy_target in buy_source:
        buy_array.append(buy_target.text.strip())
    for sale_target in sale_source:
        sale_array.append(sale_target.text.strip())

    return(buy_array, sale_array)

def answer_string():
    buy_array_result = get_current_exchange_rate()[0]
    sale_array_result = get_current_exchange_rate()[1]

    if not buy_array_result[1] and sale_array_result[1]:
        buy_array_result.insert(1, "0") and sale_array_result.insert(1, "0")
    if not buy_array_result[3] and sale_array_result[3]:
        buy_array_result.insert(3, "0") and sale_array_result.insert(3, "0")    

    return("🕐\f" + update_time() + "\n____________________________"
           "\n\nСередня купівля:" + "\n💵 1 USD = " + buy_array_result[0] + "\fUAH" + "\f[%s ₴]" % buy_array_result[1] +
           "\nСередній продаж:" + "\n💵 1 USD = " + sale_array_result[0] + "\fUAH" + "\f[%s ₴]" % sale_array_result[1] + 
           "\n\nСередня купівля:" + "\n💶 1 EUR = " + buy_array_result[2] + "\fUAH" + "\f[%s ₴]" % buy_array_result[3] +
           "\nСередній продаж:" + "\n💶 1 EUR = " + sale_array_result[2] + "\fUAH" + "\f[%s ₴]" % sale_array_result[3])                     

#def graph():

bot.polling(none_stop=True, interval=0) 

   