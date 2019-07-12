# coding=utf-8

import json


def announcement(bot, update, mensaje):

    with open("users/usuarios") as f:
        lista_usuarios = json.load(f)

    for idTelegram in lista_usuarios:
        try:
            bot.send_message(idTelegram, mensaje, parse_mode="Markdown")
        except:
            update.message.reply_text("No se ha podido enviar el mensaje a %s" % idTelegram)
