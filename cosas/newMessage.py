#coding=utf-8

import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode


class NewMessage:

    def __init__(self):
        with open("newMessages") as f:
            self.newMessages = json.load(f)

    def normal(self, bot, update, Usuarios):
        query = update.callback_query

        Usuarios.actualizarUsuario(update.callback_query.from_user.id,4)
        Usuarios.actualizarMensaje(update.callback_query.from_user.id, init="normal")

        msg="Estas escribiendo un mensaje de tipo normal (de un sólo texto). Usa /cancel para cancelar.\n*RECUERDA:* Si q" \
            "uieres poner nombres de jugadores usa {1} para el primer nombre aleatorio y {2} para el segundo nombre."

        keyboard = [[InlineKeyboardButton("AYUDA 🆘", url="telegra.ph/Okay-03-12")]]

        bot.edit_message_text(text=msg,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def RI(self, bot, update, Usuarios):
        query = update.callback_query

        Usuarios.actualizarUsuario(update.callback_query.from_user.id,5)
        Usuarios.actualizarMensaje(update.callback_query.from_user.id, init="RI")

        msg="Estas escribiendo un mensaje de tipo RI (dos mensajes seguidos). Usa /cancel para cancelar.\n*RECUERDA:* Si q" \
            "uieres poner nombres de jugadores usa {1} para el primer nombre aleatorio y {2} para el segundo nombre."

        keyboard = [[InlineKeyboardButton("AYUDA 🆘", url="telegra.ph/Okay-03-12")]]

        bot.edit_message_text(text=msg,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def RNI(self, bot, update, Usuarios):
        query = update.callback_query

        Usuarios.actualizarUsuario(update.callback_query.from_user.id,6)
        Usuarios.actualizarMensaje(update.callback_query.from_user.id, init="RNI")

        msg="Estas escribiendo un mensaje de tipo RNI (dos mensajes separados). Usa /cancel para cancelar.\n*RECUERDA:* Si q" \
            "uieres poner nombres de jugadores usa {1} para el primer nombre aleatorio y {2} para el segundo nombre."

        keyboard = [[InlineKeyboardButton("AYUDA 🆘", url="telegra.ph/Okay-03-12")]]

        bot.edit_message_text(text=msg,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def picante(self, bot, update, Usuarios):
        query = update.callback_query

        posUsu = Usuarios.finder(query.from_user.id)
        editando = Usuarios.usuariosActivos[posUsu]["editando"]

        variantesActuales = editando["variantes"]

        if "picante" not in variantesActuales:
            editando["variantes"].append("picante")
            picante = True
        else:
            editando["variantes"].remove("picante")
            picante = False

        if "hastaElFondo" in variantesActuales:
            hef = True
        else:
            hef = False

        keyboard = self.categorias_generarKeyboard(picante, hef)

        bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    def hef(self, bot, update, Usuarios):
        query = update.callback_query

        posUsu = Usuarios.finder(query.from_user.id)
        editando = Usuarios.usuariosActivos[posUsu]["editando"]

        variantesActuales = editando["variantes"]

        if "hastaElFondo" not in variantesActuales:
            editando["variantes"].append("hastaElFondo")
            hef = True
        else:
            editando["variantes"].remove("hastaElFondo")
            hef = False

        if "picante" in variantesActuales:
            picante = True
        else:
            picante = False

        keyboard = self.categorias_generarKeyboard(picante, hef)

        bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    def done(self, bot, update, Usuarios, newMessages):
        query = update.callback_query

        msg = "Gracias por tu aportación, el mensaje ha pasado a revisión.\nUsa /revisar para ver mensajes en revisión."

        keyboard = [[]]

        bot.edit_message_text(text=msg,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard))

        posUsu = Usuarios.finder(query.from_user.id)
        newMessages.append(Usuarios.usuariosActivos[posUsu]["editando"])
        Usuarios.usuariosActivos[posUsu]["posicion"] = 0
        Usuarios.usuariosActivos[posUsu]["editando"] = None

    @staticmethod
    def categorias_generarKeyboard(picante, hef):
        keyboard = [[],[InlineKeyboardButton("Hecho 👌", callback_data="newMessage_done")]]

        if picante == True:
            keyboard[0].append(InlineKeyboardButton("Picante ✅", callback_data="newMessage_picante"))
        else:
            keyboard[0].append(InlineKeyboardButton("Picante ❎", callback_data="newMessage_picante"))

        if hef == True:
            keyboard[0].append((InlineKeyboardButton("Hasta el fondo ✅", callback_data="newMessage_hef")))
        else:
            keyboard[0].append(InlineKeyboardButton("Hasta el fondo ❎", callback_data="newMessage_hef"))

        return keyboard