#coding=utf-8

import random, json, logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode


class Puntos:
    """VECTOR ORINTADO A LA PUNTUACIÓN DE UN MENSAJE"""

    def __init__(self, tupla):


        self.puntos = tupla

    def __add__(self, other):

        logging.info(str(self.puntos) + str(other.puntos))
        self.puntos = (round(self.puntos[0] + other.puntos[0], 1), round(self.puntos[1] + other.puntos[1], 1))

        return self.puntos


class Revisar:
    """OBJETO DONDE SE ORGANIZAN LOS MÉTODOS PARA LA REVISIÓN DE MENSAJES"""

    def __init__(self, nUsuarios):

        self.nUsuarios = nUsuarios
        self.aceptados = []

        with open("revision.json") as f:
            self.revision = json.load(f)

    def generarKeyboard(self, msgID):

        keyboard = [[InlineKeyboardButton("1️⃣⬇️", callback_data="revisar_1down-%s" % msgID),
                     InlineKeyboardButton("0️⃣", callback_data="revisar_skip-%s" % msgID),
                     InlineKeyboardButton("1️⃣⬆️", callback_data="revisar_1up-%s" % msgID),
                     InlineKeyboardButton("2️⃣⬆️", callback_data="revisar_2up-%s" % msgID)],

                    [InlineKeyboardButton("🔙 enviar a corregir️", callback_data="revisar_rev-%s" % msgID)]]

        return keyboard

    def extraerID(self, update):
        """Este método extrae la id del mensaje del callback"""

        return update.callback_query.data.split("-")[1]

    def elegirMensaje(self, newMessages, idUSU):

        if not len(newMessages):
            return None, None
        pic = random.randint(0,len(newMessages) - 1)

        antiLoop = 0
        while idUSU in newMessages[pic]["revisar"]["revisado"]:
            pic = random.randint(0, len(newMessages) - 1)

            antiLoop += 1
            if antiLoop > 150:
                return None, None

        return newMessages[pic]["id"], pic

    def comprobarAptitutd(self, msgINDX, newMessages):

        puntos = tuple(newMessages[msgINDX]["revisar"]["puntos"])

        ptsA = self.nUsuarios * 0.6

        if puntos[0] >= round(ptsA):
            completo = newMessages.pop(msgINDX)

            completo.pop("revisar")

            self.aceptados.append(completo)
        elif puntos[0] <= round(-ptsA / 3):
            newMessages.pop(msgINDX)
        elif puntos[1] <= round(-ptsA / 3):
            completo = newMessages.pop(msgINDX)

            self.revision.append(completo)

    def updown(self, bot, update, points, newMessages):
        """Función que actualiza los puntos de X mensaje"""

        msgID = self.extraerID(update)

        query = update.callback_query

        msgINDX = self.msgFinder(msgID, newMessages)

        if msgINDX != None:
            if not query.from_user.id in newMessages[msgINDX]["revisar"]["revisado"]: # Comprobamos si el usuario ya había votado este mensaje
                points = Puntos(points)
                old = Puntos(newMessages[msgINDX]["revisar"]["puntos"])
                old + points

                newMessages[msgINDX]["revisar"]["revisado"].append(query.from_user.id)
                revisado = newMessages[msgINDX]["revisar"]["revisado"]


                newValue = {"puntos":old.puntos, "revisado":revisado}

                newMessages[msgINDX]["revisar"].update(newValue)

                self.comprobarAptitutd(msgINDX, newMessages)


        self.enviarMensaje(newMessages, bot, update, True)

    def msgFinder(self, msgID, newMessages):

        i = 0
        for e in newMessages:
            if e["id"] == msgID:
                return i
            i += 1

        return None

    def generarTexto(self, msgINDX, newMessages):
        """Este método genera el texto que tiene que llevar el mensaje."""

        if "text0" in newMessages[msgINDX]:
            msg1 = newMessages[msgINDX]["text0"]
            msg2 = newMessages[msgINDX]["text1"]
            msg = u"*Mensaje múltiple. Primer mensaje:*\n\"{0}\"\n*Segundo mensaje:*\n\"{1}\"\n"
            msg = msg.format(msg1, msg2)
        else:
            msg = "\"%s\"\n" % newMessages[msgINDX]["text"]


        if "variantes" in newMessages[msgINDX]:

            varText = ""

            for e in newMessages[msgINDX]["variantes"]:
                varText += " %s" % e

            msg += "*Variantes:%s*" %varText

        else:

            msg += "*No se han indicado variantes.*"

        return msg

    def enviarMensaje(self, newMessages, bot, update, refresh=False):

        if refresh:
            idUSU = update.callback_query.from_user.id
        else:
            idUSU = update.message.from_user.id

        msgID, msgINDX = self.elegirMensaje(newMessages, idUSU)

        if msgID != None:
            msg = self.generarTexto(msgINDX, newMessages)

            keyboard = self.generarKeyboard(msgID)
        else:
            msg = "Parece que ya has revisado todos los mensajes. Prueba más tarde."

            keyboard = [[]]

        if refresh:

            bot.edit_message_text(text=msg,
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.MARKDOWN)

        else:

            update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)