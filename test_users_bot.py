import json
from secrets import token_urlsafe
from faker import Faker
from telebot import TeleBot, types

TOKEN = '5812881681:AAGuTP-mVq1LGlYIDZLcYkiV2Cdw210Va7w'
bot = TeleBot(TOKEN, parse_mode='html')
faker = Faker('ru_RU') 

main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

main_menu_reply_markup.row(
    types.KeyboardButton(text="1️⃣"), types.KeyboardButton(text="2️⃣")
)
main_menu_reply_markup.row(
    types.KeyboardButton(text="5️⃣"), types.KeyboardButton(text="🔟")
)
main_menu_reply_markup.row(
    types.KeyboardButton(text="VISA"), types.KeyboardButton(text="MASTERCARD")
)

@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!\nЭто бот для генерации тестовых пользователей. "\
        "Выбери сколько пользователей тебе нужно 👇🏻",
        reply_markup=main_menu_reply_markup
    )

@bot.message_handler()
def message_handler(message: types.Message):
    payload_len = 0
    if message.text == "1️⃣":
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    elif message.text == 'VISA':
        bot.send_message(chat_id=message.chat.id, text=f'Тестовая карта VISA:\n<code>{faker.credit_card_number(card_type = "visa")}</code>'
        )
    elif message.text == 'MASTERCARD':
        bot.send_message(chat_id=message.chat.id, text=f'Тестовая карта MASTERCARD:\n<code>{faker.credit_card_number(card_type = "mastercard")}</code>'
        )
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
        return

    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Если нужны еще данные, можешь выбрать еще раз 👇🏻",
        reply_markup=main_menu_reply_markup
    )

def main():
    bot.infinity_polling()
if __name__ == '__main__':
    main()