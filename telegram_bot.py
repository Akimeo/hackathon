from telegram.ext import Updater, CommandHandler
from werkzeug.security import check_password_hash
from db import db, UsersModel


help_s = """
Телеграм бот для сайта UnderTask.

/start - запуск бота
/help - помощь

v0.2.0
"""


def start(bot, update):
    usid = update.message['chat']['id']
    user = UsersModel.query.filter_by(tg_id=usid)
    if user:
        update.message.reply_text(
            "Добрый день, " + user.name
        )
    else:
        update.message.reply_text(
            "Необходима авторизация через команду \"/auth логин пароль\"" +
            user.name
        )


def help(bot, update):
    update.message.reply_text(help_s)


def auth(bot, update):
    usid = update.message['chat']['id']
    user = UsersModel.query.filter_by(tg_id=usid).first()
    if user:
        update.message.reply_text(
            "Вы уже авторизованы в системе"
        )
    else:
        mes = update.message.text.split()
        if len(mes) != 3:
            update.message.reply_text('Ошибка: неверное число аргументов')
            return
        else:
            login, password = mes[1:]
            user = UsersModel.query.filter_by(name=login).first()
            if user and check_password_hash(user.password_hash, password):
                user.tg_id = usid
                db.session.commit()
                update.message.reply_text("Добро пожаловать, " + login)
            else:
                update.message.reply_text("Неверный логин или пароль.")


def tasks(bot, update):
    usid = update.message['chat']['id']
    user = UsersModel.query.filter_by(tg_id=usid).first()
    if user:
        update.message.reply_text("Задач пока нет.")
    else:
        update.message.reply_text("Ошибка: вы не авторизованы.")


def main():
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("auth", auth))
    dp.add_handler(CommandHandler("task", tasks))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    token = '792425593:AAGlpfc1SpGd9l0TRx2llhpe72wmjBO6QIM'
    main()
