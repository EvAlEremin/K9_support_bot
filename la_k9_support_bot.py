import re
import telebot
from telebot import types  # для указания типов

laK9ChatId = '-##########'  # ID чата техподдержки

botToken = '######:##################'  # токен телеграм-бота

bot = telebot.TeleBot(botToken)

welcomeMessage = '''Привет, {0.first_name}!\n
Это бот техподдержки кинологического направления ДПСО "ЛизаАлерт".
Если у вас возник вопрос, пожалуйста, напишите нам через диалоговое окно'''

links = [
    {"name": "Информация о направлении", "site": "https://lizaalert.org/forum/viewforum.php?f=296"},
    {"name": "Анкета кинолога", "site": "http://собаки-спасатели.рф/k9la-form"},
    {"name": "Отчет о работе расчета", "site": "http://собаки-спасатели.рф/reports"},
    {"name": "Запись на испытания", "site": "http://собаки-спасатели.рф/attestations"},
    {"name": "Группа K9 ЛА в Telegram", "site": "https://t.me/#####"},
    {"name": "Статистика по выездам",
     "site": "https://docs.google.com/spreadsheets/d/############################"},
    {"name": "Партнерские программы",
     "site": "https://docs.google.com/spreadsheets/d/############################"},
    {"name": "Правила аттестации",
     "site": "https://lizaalert.org/forum/viewtopic.php?f=296&t=55100&sid=764a93376ebe7972ae3ec7552b1e99c9"}
]


@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Полезные ссылки')
    item2 = types.KeyboardButton('Контакты')

    markup.row(item1, item2)

    links_description = '\n'

    for link in links:
        links_description = links_description + link["name"] + '\n'

    bot.send_message(m.chat.id, welcomeMessage.format(m.from_user, links_description), reply_markup=markup)


# Получение сообщений
@bot.message_handler(content_types=["text"])
def handle_text(m):
    # здесь если чат id равен id чата поддержки, то отправить сообщение пользователю который задал вопрос
    if int(m.chat.id) == int(laK9ChatId):
        if (m.reply_to_message is not None):
            chatId = get_chat_id(m.reply_to_message.text)
            if chatId is not None:
                bot.send_message(chatId, m.text)

    elif m.text == 'Полезные ссылки':
        markup_links = types.InlineKeyboardMarkup()
        for link in links:
            markup_links.row(types.InlineKeyboardButton(link["name"], url=link["site"]))

        bot.send_message(m.chat.id, 'Полезные ссылки', reply_markup=markup_links)

    elif m.text == 'Контакты':
        markup_cont = types.InlineKeyboardMarkup()
        cont1 = types.InlineKeyboardButton('Посмотреть', url='https://lizaalert.org/forum/viewtopic.php?f=296&t=64243')
        markup_cont.add(cont1)
        bot.send_message(m.chat.id, 'Контакты старших направления', reply_markup=markup_cont)

    else:
        bot.send_message(laK9ChatId,
                         "Chat id: {0}\nFull name: {1}\nUsername: @{2}\n\n{3}".format(m.chat.id, m.from_user.full_name,
                                                                                      m.from_user.username, m.text))


def get_chat_id(message):
    first_line = message.split('\n')[0]
    if first_line is not None:
        return first_line.replace('Chat id: ', '')

if __name__ == '__main__':
    bot.infinity_polling(timeout=10, long_polling_timeout=5)