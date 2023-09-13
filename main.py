import telebot
from telebot.types import *

with open("C:\\tg_token_@inv_dist_bot.txt", 'r') as token:
    bot = telebot.TeleBot(*token)


@bot.message_handler(commands=['start'])
def user_start(message):
    msg = 'Привет. Я умею инвертировать сообщения [/inv], а также искажать сообщения сЛеДуЮщИм ОбРаЗоМ [/dist]'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['inv'])
def user_inv(message):
    msg = bot.send_message(message.chat.id, 'Я ожидаю сообщение, которое нужно перевернуть...')
    bot.register_next_step_handler(message, invert, msg)


def invert(message, msg_for_del):
    bot.delete_message(msg_for_del.chat.id, msg_for_del.message_id)

    msg = message.text[::-1]
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['dist'])
def user_dist(message):
    kb = InlineKeyboardMarkup()
    kb_yb = InlineKeyboardButton(text='Заглавная', callback_data='y')
    kb_nb = InlineKeyboardButton(text='Строчная', callback_data='n')
    kb.add(kb_yb, kb_nb)

    bot.send_message(message.chat.id, 'Первая буква заглавная или строчная?', reply_markup=kb)


@bot.callback_query_handler(func=lambda callback: callback.data in ['y', 'n'])
def callback_dist_yn(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, 'Ожидаю от Вас сообщение...')
    if call.data == 'y':
        bot.register_next_step_handler(call.message, dist_fir, msg)
    elif call.data == 'n':
        bot.register_next_step_handler(call.message, dist_sec, msg)


def dist_fir(message, msg_for_del):
    bot.delete_message(msg_for_del.chat.id, msg_for_del.message_id)

    even = message.text[::2]
    odd = message.text[1::2]

    msg = ''

    upper_list = even.upper()
    lower_list = odd.lower()

    for i in range(len(message.text)):
        if i % 2 == 0:
            num = int(i / 2)
            msg += upper_list[num]
        else:
            num = int((i - 1) / 2)
            msg += lower_list[num]

    bot.send_message(message.chat.id, msg)


def dist_sec(message, msg_for_del):
    bot.delete_message(msg_for_del.chat.id, msg_for_del.message_id)

    even = message.text[::2]
    odd = message.text[1::2]

    msg = ''

    upper_list = odd.upper()
    lower_list = even.lower()

    for i in range(len(message.text)):
        if i % 2 == 0:
            num = int(i / 2)
            msg += lower_list[num]
        else:
            num = int((i - 1) / 2)
            msg += upper_list[num]

    bot.send_message(message.chat.id, msg)


if __name__ == "__main__":
    print('start')
    bot.infinity_polling()