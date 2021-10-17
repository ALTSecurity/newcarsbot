# -*- coding: cp1251 -*-
import os
import telebot
from flask import Flask, request
from telebot import types

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
server = Flask(__name__)

documents_text = "В усіх перелічених випадках разом з митною декларацією (оформлюється митним брокером) на транспортний засіб, що декларується в режим імпорту (вільний обіг), подаються такі основні документи:\n- реєстраційні (технічні) документи на транспортний засіб (як правило, це технічний паспорт);\n- документи, що підтверджують право власності особи на транспортний засіб (як правило, це договір купівлі-продажу) або право ним розпоряджатися та декларувати (як правило, це доручення);\n- рахунок-фактуру (інвойс) або інший документ, який визначає вартість товару (можливо, це буде один і той же документ, що підтверджує право власності)."
place_text = "Митне оформлення можна здійснити у будь-якій митниці України.\nАдреси та реквізити конкретних місць оформлення можна знайти на субсайтах територіальних органів ДФС або на веб-порталі ДФС."
own_text = "Можна не виїжджати, а подати необхідні документи і пред’явити транспортний засіб у будь-яку митницю (найближчу)."
discount_text = "Знижка протягом 90 днів (тобто коефіцієнт 0,5 при сплаті акцизного податку) може бути застосована при оформленні громадянином лише одного легкового транспортного засобу.\nОдин транспортний засіб може бути оформлений тільки один раз. Якщо автомобіль вже був оформлений митницею раніше та сплачені платежі, то оформити цей же автомобіль ще раз і скористатись знижкою (коефіцієнт 0,5) неможливо."
broker_text = "Теоретично громадянин може спробувати самостійно заповнити митну декларацію та подати необхідні документи (законодавством це не забороняється).\nАле краще звернутись до митного брокера – до кваліфікованого спеціаліста, оскільки законодавством передбачено, що транспортні засоби декларуються із заповненням митної декларації, порядок заповнення якої потребує спеціальних знань та певного програмного забезпечення. Крім того, паперова митна декларація повинна обов’язково супроводжуватись її електронною копією."

@bot.message_handler(commands=['start', 'help'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привіт, я допоможу тобі розібратись з правилами щодо розмитнення автомобілів з іноземною реєстрацією.")
    keyboard = types.InlineKeyboardMarkup()
    key_docs = types.InlineKeyboardButton(text='Документи, що необхідні для ввезення авто', callback_data='documents')
    keyboard.add(key_docs)
    key_place = types.InlineKeyboardButton(text='Де розмитнити автомобіль', callback_data='place')
    keyboard.add(key_place)
    key_own = types.InlineKeyboardButton(text='Оформлення в митниці свого регіону', callback_data='own')
    keyboard.add(key_own)
    key_discount = types.InlineKeyboardButton(text='Знижка', callback_data='discount')
    keyboard.add(key_discount)
    key_broker = types.InlineKeyboardButton(text='Самостійна подача документів', callback_data='broker')
    keyboard.add(key_broker)
    bot.send_message(message.from_user.id, text='Вибери питання, що тебе цікавить', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "documents":
        bot.send_message(call.message.chat.id, documents_text)
    elif call.data == "place":
        bot.send_message(call.message.chat.id, place_text)
    elif call.data == "own":
        bot.send_message(call.message.chat.id, own_text)
    elif call.data == "discount":
        bot.send_message(call.message.chat.id, discount_text)
    elif call.data == "broker":
        bot.send_message(call.message.chat.id, broker_text)

@server.route('/' + token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/", methods=['POST'])
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://newcarsbot.herokuapp.com/' + token)
    return "!", 200
# Запускаем постоянный опрос бота в Телеграме
#bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
