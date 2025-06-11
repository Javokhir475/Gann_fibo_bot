
import os
import telebot
import math
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Gann hisoblash
def gann_levels(price, direction):
    sqrt_price = math.sqrt(price)
    levels = []

    steps = [-0.125, -0.25, -0.5, -0.625] if direction == 'sell' else [0.125, 0.25, 0.5, 0.625]
    for step in steps:
        level = round((sqrt_price + step) ** 2, 2)
        levels.append(level)

    sl = round((sqrt_price - 0.125) ** 2, 2) if direction == 'buy' else round((sqrt_price + 0.125) ** 2, 2)
    return levels, sl

# Fibonacci hisoblash
def fibonacci_levels(high, low, direction):
    diff = high - low
    retracements = [0.5, 0.618, 0.786]
    entries = [round(high - diff * r, 2) for r in retracements]

    extensions = [1, 1.618, 1.786, 1.88, 2.11, 2.25, 2.618, 2.786, 2.88]
    tps = [round(low - diff * e, 2) for e in extensions] if direction == 'sell' else [round(high + diff * e, 2) for e in extensions]

    return entries, tps

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Ganna", "Fibonacci")
    bot.send_message(message.chat.id, "Qaysi hisob-kitobni ishlatmoqchisiz?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    if text.startswith("/buy") or text.startswith("/sell"):
        parts = text[1:].split()
        direction = parts[0]
        if len(parts) == 2:
            try:
                price = float(parts[1])
                levels, sl = gann_levels(price, direction)
                bot.send_message(message.chat.id, f"Gann {direction.upper()} signal:
TP1: {levels[0]}
TP2: {levels[1]}
TP3: {levels[2]}
TP4: {levels[3]}
SL: {sl}")
            except:
                bot.send_message(message.chat.id, "Narx noto‘g‘ri kiritildi.")
        elif len(parts) == 3:
            try:
                high = float(parts[1])
                low = float(parts[2])
                entries, tps = fibonacci_levels(high, low, direction)
                entry_text = "\n".join([f"Entry {i+1}: {e}" for i, e in enumerate(entries)])
                tp_text = "\n".join([f"TP{i+1}: {tp}" for i, tp in enumerate(tps)])
                bot.send_message(message.chat.id, f"Fibonacci {direction.upper()} signal:
{entry_text}
{tp_text}")
            except:
                bot.send_message(message.chat.id, "High va Low qiymatlar noto‘g‘ri kiritildi.")
        else:
            bot.send_message(message.chat.id, "Noto‘g‘ri buyruq formati.")
    else:
        bot.send_message(message.chat.id, "Iltimos, Ganna yoki Fibonacci tugmasini tanlang yoki /buy yoki /sell bilan buyruq yuboring.")

bot.infinity_polling()
