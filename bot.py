import requests
import telebot
import config
import time


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    file = open("id.txt", "w")
    file.write(str(chat_id))
    file.close()


@bot.message_handler(commands=['start_send_order'])
def start_send_order():
    send_message(20)


def send_message(time_out):
    last_time = time.time()
    while True:
        if time.time() - last_time > time_out:

            file = open("../bot_for_admins/id.txt", "r")
            chat_id = file.read()
            file.close()
            orders = requests.get("https://hookah-batumi.herokuapp.com/set_orders/5000").json()
            if orders:
                for el in orders:
                    message = "Номер заказа: #" + str(orders[el]["id"]) + "\nЗаказ: " + str(orders[el]["order_el"]) + "\nИмя: " + str(orders[el]["name"]) + "\nАдрес: " + str(orders[el]["address"]) + "\nТелефон: " + str(orders[el]["phone"]) + "\nМессенджер: " + str(orders[el]["messenger"]) + "\nКомментарий: " + str(orders[el]["comment"]) + "\nОбщая стоимость: " + str(orders[el]["order_price"])
                    bot.send_message(int(chat_id), message)

            last_time = time.time()


bot.polling(none_stop=True)