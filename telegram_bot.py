from telegram.ext import Updater, CommandHandler
from werkzeug.security import check_password_hash
from db import UsersModel


help_s = """
Телеграм бот для сайта UnderTask.

/start - запуск бота
/help - помощь

v0.1.0
"""


def start(bot, update):
    update.message.reply_text(
        "Для подробной информации введите /help"
    )


def help(bot, update):
    update.message.reply_text(help_s)


def auth(bot, update):
    try:
        update.message.reply_text(str(update.message.user_id))
    except Exception:
        update.message.reply_text(str(update.message))


def main():
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("auth", auth))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    token = '792425593:AAGlpfc1SpGd9l0TRx2llhpe72wmjBO6QIM'
    main()
