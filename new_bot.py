from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


pipeline = joblib.load('classifier.joblib.pkl')



def answer(pipeline, temp_text):
    answer = pipeline.predict(temp_text)
    return answer



import Function as F
import pandas as pd
import numpy as np
import random
import win32com.client

import telebot
import markups as m


#main variables
TOKEN = '874682186:AAGUglxyYvimOo8bh2UzEbHTeehAzvLgAi8'
bot = telebot.TeleBot(TOKEN)




#handlers
@bot.message_handler(commands=['start', 'go'])
def start_handler(message):

    isRunning = False

    if not isRunning:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Привет', reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        isRunning = True

def askWhattodo(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text == 'привет':
        msg = bot.send_message(chat_id, 'Как дела? Пиши максимально подробно', reply_markup=False)
        bot.register_next_step_handler(msg, p_n)
    else:
        msg = bot.send_message(chat_id, 'Нажми привет', reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        return
    #isRunning = False

def p_n(message):
    chat_id = message.chat.id
    text = message.text.lower()
    text = [text]
    ans=answer(pipeline, text)
    print(ans)
    if ans == -1:
        msg = bot.send_message(chat_id, 'Я правильно понял, что тебе грустно?', reply_markup=m.yes_or_no_markup )
        bot.register_next_step_handler(msg, sad)
    else:
        msg = bot.send_message(chat_id, 'Я правильно понял, что у тебя все хорошо?', reply_markup=m.yes_or_no_markup)
        bot.register_next_step_handler(msg, good)
    #isRunning = False

def sad(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text == 'да':
        msg = bot.send_message(chat_id, 'Тогда я тебе подниму настроение! Выбирай какой анекдот ты хочешь', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
    elif text == 'нет':
        msg = bot.send_message(chat_id, 'Отлично! У тебя хорошее настсроние. Лови анекдот, только сначала выбери какой ты хочешь', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
    else:
        msg = bot.send_message(chat_id, 'Я не знаю как на это ответит, давай начнем сначала. Нажми привет', reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        return
    #isRunning = False
number=0
def askSource(message):
    chat_id = message.chat.id
    text = message.text.lower()

    if text == 'по категориям':
        msg = bot.send_message(chat_id, 'Выбирай категорию', reply_markup=m.category_markup)
        bot.register_next_step_handler(msg, category)
    elif text == 'лучшие':
        ans=F.top()[0]
        n=F.top()[1]
        F.ap(chat_id, n, F.dictionary)
        msg = bot.send_message(chat_id, 'Держи анекдот \n' + ans + '\n оцени его, пожалуйста, по шкале от 1 до 5', reply_markup=m.raiting_markup)
        bot.register_next_step_handler(msg, raiting)
    else:
        msg = bot.send_message(chat_id, 'Я не знаю как на это ответит, давай начнем сначала. Нажми привет',reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        return
    #isRunning = False


def good(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text == 'нет':
        msg = bot.send_message(chat_id, 'Оу( Тебе грустно. Тогда я тебе подниму настроение! Выбирай какой анекдот ты хочешь', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
    elif text == 'да':
        msg = bot.send_message(chat_id, 'Отлично! У тебя хорошее настроние. Лови анекдот, только сначала выбери какой ты хочешь', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
    else:
        msg = bot.send_message(chat_id, 'Я не знаю как на это ответит, давай начнем сначала. Нажми привет', reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        return
    #isRunning = False



def category(message):
    "лист категорий анекдотов"
    list = ['о водителях', 'общественный транспорт', 'об адвокатах и судьях', 'василий иваныч и петька', 'про актеров и актрис', 'животные','о браке', 'армия', 'о вовочке', 'о жизни']
    chat_id = message.chat.id
    text = message.text.lower()
    if text in list:
        ans=F.category(text)[0]
        n=F.category(text)[1]
        F.ap(chat_id, n, F.dictionary)
        msg = bot.send_message(chat_id, 'Держи анекдот \n'+ ans + '\n оцени его, пожалуйста, по шкале от 1 до 5', reply_markup=m.raiting_markup)
        bot.register_next_step_handler(msg, raiting)
    elif text == 'б':
        ans1=F.category_B()
        msg = bot.send_message(chat_id, 'Это можно читать если тебе есть 18 лет. \n' + ans1 + '', reply_markup=m.whattodo_markup)
        bot.register_next_step_handler(msg, whattodo)
    else:
        msg = bot.send_message(chat_id, 'Я не знаю как на это ответит, давай начнем сначала. Нажми привет', reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        return
    #isRunning = False

def raiting(message):

    list = ['1', '2', '3', '4', '5']
    chat_id = message.chat.id
    text = message.text.lower()
    if text in list:
        number=F.number(chat_id, F.dictionary)
        F.ranking(int(text), int(number))

        msg = bot.send_message(chat_id, 'Спасибо за оценку, что ты еще хочешь?', reply_markup=m.whattodo_markup)
        bot.register_next_step_handler(msg, whattodo)
    else:
        msg = bot.send_message(chat_id, 'Я не знаю как на это ответит, давай начнем сначала. Нажми привет', reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        return




def whattodo(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text == 'хочу еще анекдот':
        msg = bot.send_message(chat_id, 'Тогда выбирай какой анекдот ты хочешь:)', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
    elif text == 'я тебя люблю':
        msg = bot.send_sticker(chat_id, 'CAADAgADUAoAAi8P8AbtFYE7sWqtpAI')
        bot.register_next_step_handler(msg, whattodo)
    elif text == 'общесос':
        msg = bot.send_sticker(chat_id, 'CAADAgADYQADL0lHCVo2hh1S-ywmAg')
        bot.register_next_step_handler(msg, whattodo)
    elif text =='мне от тебя ничего не надо':
        msg = bot.send_message(chat_id, 'Прощай, возвращайся, когда захочешь анекдот)')
        bot.register_next_step_handler(msg, whattodo)
    elif text == 'крушить':
        msg = bot.send_sticker(chat_id, 'CAADAgADigYAAtJaiAG9HFinsr5dqQI')
        bot.register_next_step_handler(msg, whattodo)
    else:
        msg = bot.send_message(chat_id, 'Я не знаю как на это ответит, давай начнем сначала. Нажми привет', reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, askWhattodo)
        return
    #isRunning = False


bot.polling(none_stop=True)