from telebot import types
import urllib3
import telebot
from urllib.request import urlopen
import json
import urllib.parse
from telegram import Update
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import MessageHandler
import os
from flask import Flask, request
import mysql.connector
import threading
import urllib.request

# from mysql.connector import Error

# mydb = mysql.connector.connect(host="ikino.cxutdxbu2lll.eu-west-2.rds.amazonaws.com", user='adminroot', passwd='adminroot', database='mydatabase')
# mycursor = mydb.cursor()

# bot = telebot.TeleBot("1030009658:AAF2BcUKWm7lTAdQ2CRq27ycHI4qJfKculs")
# TOKEN = '1030009658:AAF2BcUKWm7lTAdQ2CRq27ycHI4qJfKculs'

bot = telebot.TeleBot("1186768647:AAHAQ23Jb1U6MTK203bxXC_-I6OuJusZ-3s")
TOKEN = '1186768647:AAHAQ23Jb1U6MTK203bxXC_-I6OuJusZ-3s'


eror = '🤷‍♂️*Результатов не найдено. Возможно фильма или сериала с таким названием нет или вы ввели название с ошибкой.*'\
        '\n' \
        '\n' \
        'Попробуйте еще раз! Отправьте мне название фильма или сериала как оно пишется в Кинопоиске. *Год фильма или сериала, какой сезон и какая серия при поиске писать не нужно!!*'  \
        "\n" \
        "\n" \
        "_Задать вопросы или пообщаться можно в нашем чате_" + '👉 [@Kino_Chat]'+"(https://t.me/kino_chat)"

podptext = 'Привет друзья! Наш бот абсолютно бесплатен и без рекламы! Но доступ у него открыт только подписчикам нашего канала👉 '+ '[ФИЛЬМЫ И СЕРИАЛЫ]'+'(@filmy_1080)' \
            "\n" \
            "\n" \
            'Подпишитесь, что бы не пропускать новинки! *После подписки нажмите кнопку "Я подписался". Доступ будет открыт автоматически.*'

privet = "👋Добро пожаловать в поиск! Напиши мне название фильма, мультфильма или сериала и я найду их для тебя." \
             "\n" \
             "\n" \
             '❗️*ВАЖНО!* Год выпуска, номер сезона или номер серии *писать не нужно!* Название должно быть правильным (как в Кинопоиске)! В обратном случае, я ничего не смогу найти для тебя. Например:' \
             "\n" \
             "\n" \
             "*✅Правильно:*  Ведьмак" \
             "\n" \
             "*✅Правильно:* The Witcher" \
             "\n" \
             '*❌Неправильно:* Ведьмак 2019' \
             "\n" \
             '*❌Неправильно:* Ведьмак 1 сезон' \
             "\n" \
             "\n" \
             'Жду от тебя названия фильма👇'\
             "\n" \
            'Приятного просмотра!🍿'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global podptext
    global privet
    # global mydb
    # mybaza = open(imputfiles, mode='a', encoding='latin_1')

    fname = str(message.from_user.first_name)
    lname = str(message.from_user.last_name)
    userN = str(message.from_user.username)
    userId = int(message.from_user.id)
    try:
        mydb = mysql.connector.connect(host="ikino.cxutdxbu2lll.eu-west-2.rds.amazonaws.com", user='ikino_site', passwd='i06m50w3ohokodzw', database='mydatabase', port='3306')
        # if mydb.is_connected():
        mycursor = mydb.cursor()
        sqlform = 'Insert into Members2(usernames, userid, imya, famil) values(%s, %s, %s, %s)'
        Userss = [(userN, userId, fname, lname)]
        mycursor.executemany(sqlform, Userss)
        mydb.commit()
        mydb.close()
        chri = "member"
        if chri == bot.get_chat_member(chat_id="@filmy_1080", user_id=message.from_user.id).status:
            bot.send_message(message.chat.id, privet, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True)
        else:
            urlpod = "@filmy_1080"                   
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text='Подписаться ➡️', url=urlpod)
            url_button2 = types.InlineKeyboardButton(text="Я подписался 👍", callback_data='testp')
            keyboard.add(url_button)
            keyboard.add(url_button2)
            bot.send_message(message.chat.id, podptext, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True, reply_markup=keyboard)
    except mysql.connector.Error:
        bot.send_message(message.chat.id, 'Попробуйте снова. Нажмите /start', parse_mode=ParseMode.MARKDOWN)
        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global privet
    global podptext
    if call.message:
        if call.data == 'testp':
            chri = "member"
            if chri == bot.get_chat_member(chat_id="@filmy_1080", user_id = call.message.chat.id).status:
                bot.send_message(call.message.chat.id, privet, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы не подписаны на канал!🤷‍♂️ Подпишитесь!")   
# tr1 = threading.Thread(target=send_welcome).start()    
    # if userN != 'None':
    #     bot.send_message(myChat,newMember + " " +'@'+ userN, parse_mode=ParseMode.MARKDOWN)
    # else:
    #     bot.send_message(myChat,newMember + " " + userId, parse_mode=ParseMode.MARKDOWN)
    #
    # bot.forward_message(myChat, myBot, message.message_id)



# @bot.message_handler(commands=['sender'])
# def send_news(message):
#     global mydb
#     soob = "Привет, мои друзья!"
#     mycursor = mydb.cursor()
#     mycursor.execute('Select userIds from Users')
#     myresult =  mycursor.fetchall()
#     for row in myresult:
#         row = int(row[0])
#         bot.send_chat_action(row, 'typing')

#         bot.send_message(row, soob)
#         time.sleep(20)


@bot.message_handler(content_types=['text'])
def bad_poisk(message):

#     mycursor = mydb.cursor()
#     mycursor.execute('Select userIds from Users')
#     myresult =  mycursor.fetchall()
#     for row in myresult:
#         row = int(row[0])
#   for us in row:
#   if userId != 324969393 and userId != 324969393:
    global eror
    global podptext
    chri = "member"
    if message.text != "после" and message.text != "После" and message.text != "ПОСЛЕ":  
        if chri == bot.get_chat_member(chat_id="@filmy_1080", user_id=message.from_user.id).status or message.from_user.id == 324969393:
            if len(message.text)>3:
                try:
                    x = int(message.text) + 1
                    bot.send_message(message.chat.id, eror, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True)
                except ValueError:
                    userN = str(message.from_user.username)
                    userId = int(message.from_user.id)
                            
                    fname = str(message.from_user.first_name)
                    lname = str(message.from_user.last_name)
                    # try:
                    #     mydb = mysql.connector.connect(host="nbfj50setb1vgbjh.cbetxkdyhwsb.us-east-1.rds.amazonaws.com", user='ej4hz3lszccvek32', passwd='i06m50w3ohokodzw', database='d6idyikh5aoehxm1')
                    #     mycursor = mydb.cursor()
                    #     sqlform = 'Insert into Poisk(usernames, userid, zapros, imya, famil) values(%s, %s, %s, %s, %s)'
                    #     Userss = [(userN, userId, message.text, fname, lname)]
                    #     mycursor.executemany(sqlform, Userss)
                    #     mydb.commit()
                    #     mydb.close()
                    # except mysql.connector.Error:
                    #     bot.send_message(message.chat.id, 'Ух!)', parse_mode=ParseMode.MARKDOWN)

                    z = 'http://playeronline.pro/api/videos.json?title=' + urllib.parse.quote(
                        message.text) + '&token=85830ea7678f45a6647affe05b742c92'
                    try:
                        
                        # proxies = {'http': 'http://20mY2G:j3RW8y@45.87.241.152:8000'}
                        # {'http': '165.225.38.100:10605'}

                        # proxy_support = urllib.request.ProxyHandler({'http':'96.45.112.174:80'})
                        # opener = urllib.request.build_opener(proxy_support)
                        # urllib.request.install_opener(opener)
                        # with urllib.request.urlopen (z) as response:

                        with urlopen(z) as response:
                        
                            source = response.read()
                        try:

                            data = json.loads(source)
                        
                            if len(data) <= 0:
                                bot.send_message(message.chat.id, eror, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True)
                            else:
                                for i in data:
                                    if i['type'] == 'movie' and i['kinopoisk_id'] != 1049459 and i['kinopoisk_id'] != 989978 and i['kinopoisk_id'] != 1055319 and i['kinopoisk_id'] != 1183571 and i['kinopoisk_id'] != 1201533 and i['kinopoisk_id'] != 1102923 and i['kinopoisk_id'] != 809823 and i['kinopoisk_id'] != 1245524 and i['kinopoisk_id'] != 995075 and i['kinopoisk_id'] != 1281638 and i['kinopoisk_id'] != 737900 and i['kinopoisk_id'] != 1112920 and i['kinopoisk_id'] != 1371715:
                                        url1 = 'http://playeronline.pro/movie/' + i['token'] + '/iframe?d=skyfilm.org'
                                        otvet = '['+'🎥'+']'+'('+ i['poster']+')'+ '*'+i['title_ru'] + " " +'('+ str(i['year']) + '/' + i['quality'] + ')'+'*'+'\n' \
                                            +'Озвучка:' + " " + i['translator'] + '\n' + '\n' \
                                            + '[👁‍🗨СМОТРЕТЬ ФИЛЬМ]' + '('+ url1 + ')'\
                                            "\n" \
                                            "\n" \
                                            '[🔍ПОИСК ФИЛЬМОВ]' + '(https://t.me/filmy_serialy_bot)'\
                                            "\n" \
                                            "\n" \
                                            '[🎮 ИГРЫ БЕСПЛАТНО]'+ '(https://bit.ly/2J09KdU)'
                                        url2 = "https://t.me/filmy_serialy_bot"
                                        url3 = "https://t.me/joinchat/AAAAAEZFN2QP3nxwqJ-7Ng"                   
                                        keyboard = types.InlineKeyboardMarkup()
                                        url_button = types.InlineKeyboardButton(text="Смотреть фильм", url= url1)
                                        url_button2 = types.InlineKeyboardButton(text="🔍Поиск фильмов", url= url2)
                                        url_button3 = types.InlineKeyboardButton(text="🔥Лучшие Фильмы🔥", url= url3)
                                        keyboard.add(url_button)
                                        keyboard.add(url_button2)
                                        keyboard.add(url_button3)
                                        bot.send_message(message.chat.id, otvet, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = False, reply_markup=keyboard)



                                    elif i['type'] == 'serial':
                                        url1 = 'http://playeronline.pro/serial/' + i['token'] + '/iframe?d=skyfilm.org'
                                        otvet = '['+'🎥'+']'+'('+ i['poster']+')'+ '*'+i['title_ru'] + " " +'('+ str(i['year']) + '/' + i['quality'] + ')'+'*'+'\n' \
                                            +'Озвучка:' + " " + i['translator'] + '\n' + '\n' \
                                            + '[👁‍🗨СМОТРЕТЬ СЕРИАЛ]' + '('+ url1 + ')'\
                                            "\n" \
                                            "\n" \
                                            '[🔍ПОИСК ФИЛЬМОВ]' + '(https://t.me/filmy_serialy_bot)'\
                                            "\n" \
                                            "\n" \
                                            '[🎮 ИГРЫ БЕСПЛАТНО]'+ '(https://bit.ly/2J09KdU)'
                                            
                                        url2 = "https://t.me/filmy_serialy_bot"
                                        url3 = "https://t.me/joinchat/AAAAAEZFN2QP3nxwqJ-7Ng"
                                        keyboard = types.InlineKeyboardMarkup()
                                        url_button = types.InlineKeyboardButton(text="Смотреть сериал", url= url1)
                                        url_button2 = types.InlineKeyboardButton(text="🔍Поиск фильмов", url= url2)
                                        url_button3 = types.InlineKeyboardButton(text="🔥Лучшие Фильмы🔥", url= url3)
                                        keyboard.add(url_button)
                                        keyboard.add(url_button2)
                                        keyboard.add(url_button3)
                                        bot.send_message(message.chat.id, otvet, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = False, reply_markup=keyboard)
                        except json.decoder.JSONDecodeError:
                            bot.send_message(message.chat.id, "Извините, у нас технические работы на сервере. Мы скоро закончим:) Пожалуйста, вернитесь позже.", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True)                
                    except urllib.error.URLError:
                        bot.send_message(message.chat.id, "Сейчас в работе телеграм BotApi наблюдаются сбои, поэтому на ваш запрос не поступило ответа от сервера. Вы можете попробовать еще раз или вернуться позже. Приносим вам свои извинения за неудобства!", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True)       
        else:
            urlpod = "@filmy_1080"
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text='Подписаться ➡️', url=urlpod)
            url_button2 = types.InlineKeyboardButton(text="Я подписался 👍", callback_data='testp')
            keyboard.add(url_button)
            keyboard.add(url_button2)
            bot.send_message(message.chat.id, podptext, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, eror, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview = True)


tr1 = threading.Thread(target=send_welcome).start()
tr2 = threading.Thread(target=callback_inline).start()
tr3 = threading.Thread(target=bad_poisk).start()

# bot.polling(none_stop=True)

server = Flask(__name__)
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    TOKEN = '1186768647:AAHAQ23Jb1U6MTK203bxXC_-I6OuJusZ-3s'
    bot.remove_webhook()
    bot.set_webhook(url='https://evening-badlands-20190.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8443)))
