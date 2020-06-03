import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('1261035322:AAHwgXiiloxGIHn_jB12_2WpIDjiFTW0h9c')

headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

def get_time(time_zone):
    url = f'https://www.google.com/search?q={str(time_zone)}&oq={str(time_zone)}&aqs=chrome..69i57.4223j0j7&sourceid=chrome&ie=UTF-8'
    full_page = requests.get(url, headers=headers)

    soup = BeautifulSoup(full_page.content, 'html.parser')

    convert = soup.find_all('span', {'class': 'r0bn4c rQMQod'})
    return convert[1].text

@bot.message_handler(commands=['start'])
def start(message):
    send_message = f"<b>Hi, {message.from_user.first_name} {message.from_user.last_name}</b>! How are you doing?"
    bot.send_message(message.chat.id, send_message, parse_mode='html')

@bot.message_handler(commands=['timezone'])
def timezone(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton('Pacific Time Zone (US)')
    markup.add(button1)

    send_message = f"<b>Choose a Time Zone where you want to get time!</b>"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message(message):
    client_message = message.text.strip().lower()

    if (client_message == 'pacific time zone (us)'):
        time = get_time(client_message)
        bot.send_message(message.chat.id, time, parse_mode='html')

bot.polling(none_stop=True)