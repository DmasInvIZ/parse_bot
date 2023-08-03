import requests
import time
from bs4 import BeautifulSoup as bs
import telebot

TOKEN = "6476141297:AAEX-qm0JttdQrv_CcgeBSBFAF3ynqlTKHI"

bot=telebot.TeleBot(TOKEN)
url = "https://www.kufar.by/l/komplektuyushchie-dlja-kompjutera?query=core+2+duo+t9500&rgn=all&sort=lst.d&utm_filter\
Origin=Search_suggester_3&utm_queryOrigin=Manually_typed&utm_suggestionType=Category_only"
session = requests.Session()
session.trust_env = False


def check_announce():
    announce_list = []
    request = session.get(url)
    soup = bs(request.text, "lxml")
    for i in soup.find_all("section", class_=None):  # ищем все секции
        global key_title
        key_title = i.find("h3", class_="styles_title__F3uIe").text  # ищем заголовки объявлений
        global value_link
        value_link = soup.find("a", class_="styles_wrapper__5FoK7").get(
            'href')  # ищем в секциях все объявления и получаем на них ссылки
        if key_title not in announce_list:
            announce_list.append({key_title: value_link})
    return announce_list


def send_msg(message):
    chat_id = "2127625714"  # ID чата в который будет отправляться сообщение
    bot_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(bot_url).json()  # Эта строка отсылает сообщение


def check_cycle():
    while True:
        first = check_announce()
        time.sleep(30)
        second = check_announce()
        if len(first) != len(second):
            print("Количество объявлений изменилось. Сообщение в Telegram отправлено.")
            send_msg(f"Количество объявлений изменилось, вот список: {second}")
        else:
            print("Все как и было...")


if __name__ == "__main__":
    check_cycle()
