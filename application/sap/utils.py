import telebot

from application.settings import CONFIG


def send_to_telegram_channel(channel, message):
    bot = telebot.TeleBot(CONFIG['token'])
    bot.send_message(channel, text=message)