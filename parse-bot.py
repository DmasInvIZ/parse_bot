import requests
import time
from bs4 import BeautifulSoup as bs

url = "https://www.kufar.by/l/komplektuyushchie-dlja-kompjutera?query=core+2+duo+T9500&rgn=all&sort=lst.d&utm_filter\
Origin=Search_suggester_3&utm_queryOrigin=Manually_typed&utm_suggestionType=Category_only"
session = requests.Session()
session.trust_env = False


def check_announce():
    request = session.get(url)
    soup = bs(request.text, "lxml")
    announce_list = []
    for i in soup.find_all("section", class_=None):                                                 # ищем все секции
        s = i.find("a", class_="styles_wrapper__5FoK7").get('href')                                 # ищем в секциях всех объявления и получаем зи них ссылки
        announce_list.append(s)                                                                     # добавляем в массив
    print("Объявлений по запросу -", len(announce_list))
    announce_quantity = len(announce_list)
    return announce_quantity


def send_msg(message):
    TOKEN = "6476141297:AAEX-qm0JttdQrv_CcgeBSBFAF3ynqlTKHI"
    chat_id = "2127625714"                                              # ID чата в который будет отправляться сообщение
    bot_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(bot_url).json()                                                         # Эта строка отсылает сообщение


def check_cycle():
    first = check_announce()
    time.sleep(10)
    second = check_announce()
    if first is not second:
        print('Количество изменилось')
        send_msg("Количество объявлений по запросу изменилось.")


if __name__ == "__main__":
    check_cycle()
