"""
****************************************************
****************************************************
********      Author:  Mustapha Ossama     *********
********      Project: TelegramBOT         *********
********      Date:    27/11/2022          *********
****************************************************
****************************************************
"""
import telebot
from decouple import config
import requests
from bs4 import BeautifulSoup
import re
import threading
from keep_alive import keep_alive
"""
from amazon_paapi import AmazonApi
from test_settings import *
import time
"""

header = {
    "User-Agent":
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
"""
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY)
item = amazon.get_items('https://www.amazon.eg/-/en/dp/B08WJND94N')[0]
print(item.item_info.title.display_value)
"""

Telebot_API_Key = config('Telebot_API_Key')
groupID = 'AmazonePricesUpdater'
BOT = telebot.TeleBot(Telebot_API_Key)
"""
@BOT.message_handler(commands=["hello"])
def greet(message):
    BOT.send_message(message.chat.id, "OK")
"""


def sendmsg(message):
    url = f'https://api.telegram.org/bot{Telebot_API_Key}/sendMessage?chat_id=@{groupID}&text={message}'
    res = requests.get(url)


def ismsg(message):
    return True


def get_updates():
    BOT.polling(interval=10)


@BOT.message_handler(func=ismsg)
def botfunc(message):
    inputs = message.text.split()
    try:
        # read the data of that product online to compare it
        page = requests.get(inputs[0], headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')
        check = float(inputs[1]) / 2
    
        #check the unique product
        file = open('products.txt', 'r')
        lines = file.readlines()
        file.close()
        flag = 0
        for i in range(len(lines)):
            inputlink = lines[i].split()
            if inputlink[0] == inputs[0]:
                flag += 1
                lines[i] = inputs[0] + " " + inputs[1]+"\n"
                BOT.send_message(message.chat.id,"Product is Overwrited with the new price! ")
                print("\n\n\n\n\n----------------------\n")
                print(lines)
                print("--------------------")
    
        if flag > 0:
            file = open('products.txt', 'w')
            for i in lines:
                file.write(i)
    
            file.close()
        elif flag == 0:
            file = open('products.txt', 'a+')
            file.write(inputs[0] + " " + str(float(inputs[1])) + "\n")
            file.close()
            BOT.send_message(message.chat.id, "Product is added")



    except:
        BOT.send_message(message.chat.id, "Wrong Input")


polling_thread = threading.Thread(target=get_updates)
polling_thread.start()
keep_alive()
while True:
    """
    ****************************************************
    ********        Code for the BOT         *********
    ****************************************************
    """
    """
    ****************************************************
    ********        Code for the Group         *********
    ****************************************************
    """

    lineStorage = []
    file = open('products.txt', 'r+')
    lines = file.readlines()
    flag = False
    for line in lines:
        #read the data of the of a products in the product list file(products.txt)
        line = line.split()
        link = line[0]
        priceOld = line[1]

        #read the data of that product online to compare it
        try:
            page = requests.get(link, headers=header)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find(id="productTitle").get_text().strip()
            priceNew = soup.find("span", class_="a-offscreen").get_text()
            priceNew = re.findall("\d*,*\d+\.\d+", priceNew)[0]
            priceNewStack = ""
            for i in priceNew:
                if i != ',':
                    priceNewStack += i
            priceNew = float(priceNewStack)

            if float(priceOld) <= float(priceNew):
                lineStorage.append(link + " " + str(float(priceOld)))

            elif float(priceOld) > float(priceNew):
                #send telegram message
                string = "Title: " + title + '\n\n' + "New Price: " + str(
                    priceNew) + '\n\n' + "Old Price: " + str(
                        priceOld) + '\n\n' + "Link: " + link + "\n"
                sendmsg(string)

                #update the file data
                lineStorage.append(link + " " + str(float(priceNew)))
                flag = True
            for i in lines:
                print(i)
        except:
            print("Wrong Page")
            print(line)
    file.close()
    if flag:
        file = open('products.txt', 'w+')
        for line in lineStorage:
            file.write(line + "\n")
        flag = False
        file.close()
