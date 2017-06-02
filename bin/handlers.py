# coding=utf-8

import logging, random, re, uuid
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, CommandHandler
from telegram import InlineKeyboardMarkup, ParseMode
from .teclados import Menus, Teclados
from .usuarios import Usuarios
from .partida import PartidaClasica, PartidaClasicaEmparejador, ColaEmparejador
from .constantes import Constantes
from .mensaje import MensajesEnRevision, Puntos, MensajeEnRevision, MensajesClasica

def dame_mensaje_a_revisar():
    if random.randint(0, 3):
        mensaje = MensajesEnRevision.escojer_mensaje()
    else:
        mensaje = MensajesClasica.escojer_mensaje()
    return mensaje


class HandlersPiloco:

    """Handlers para las tareas del bot."""

    # GENERALES
    def mensaje(self, bot, update):

        update.message.reply_text("No sé que quieres decir.")

    def comando_start(self, bot, update):

        # TODO: comprobar si el jguador está en una partida pa no liarla parda.

        msg, keyboard = Menus.menu_principal()

        update.message.reply_text(text=msg,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.MARKDOWN)

    def menu_principal(self, bot, update):

        logging.debug("Petición para el menú principal recibida")

        msg = Menus.menu_principal()[0]
        keyboard = Menus.menu_principal()[1]

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def menu_info(self, bot, update):

        logging.debug("Petición del menú info recibida")

        msg, keyboard = Menus.menu_info(Usuarios.get_user(update.callback_query.from_user.id))

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True)

    def menu_mensajes(self, bot, update):

        msg = Menus.menu_mensajes()[0]
        keyboard = Menus.menu_mensajes()[1]

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def proximamente_clb(self, bot, update):

        update.callback_query.answer("Próximamente...")

    def restart_bot(self, bot, update):
        
        idTelegram = update.message.from_user.id
        
        usuario = Usuarios.get_user(idTelegram)
        reputacion = usuario.reputacion
        Usuarios.activos.remove(usuario)
        Usuarios._add_user(idTelegram, reputacion=reputacion)
        usuario = Usuarios.get_user(idTelegram)
        
        msg = "Se han reiniciado tus datos.\n\nNo has perdido o ganado acceso a las funciones que antes tenías\n\n" \
              "Ahora usa /start para comenzar."

        update.message.reply_text(text=msg)

        return ConversationHandler.END

    def comandos_no_soportados(self, bot, update):

        update.message.reply_text("¡Se acabaron los comandos! Piloco ya no usa interfaz por comandos, basta con que us"
                                  "es /start para ver el menú inicial o si alguna vez que el bot no responde o no hace "
                                  "lo que debería, puedes probar a usar /restart (reiniciar siempre lo arregla todo).")

    # MENSAJES
    def revisar_mensajes(self, bot, update):

        if random.randint(0,1):

            mensaje = MensajesEnRevision.escojer_mensaje(update.callback_query.from_user.id)

            if mensaje:

                if mensaje.tipo == "normal":
                    msg = u"*Mensaje simple:*\n\"%s\"" % mensaje.text

                elif mensaje.tipo == "RI":
                    msg = u"*Mensaje múltiple tipo RI 💬💬 Primer mensaje:*\n\"%s\"\n\n" \
                          u"*Segundo mensaje:*\n\"%s\"" % (mensaje.text0, mensaje.text1)

                else:
                    msg = u"*Mensaje múltiple tipo RNI 💬🕑💬 Primer mensaje:*\n\"%s\"\n\n" \
                          u"*Segundo mensaje:*\n\"%s\"" % (mensaje.text0, mensaje.text1)

                if mensaje.picante >= Constantes.PartidaClasica.VALOR_PICANTE_ALTO:
                    msg += u"\n\nSe ha indicado el mensaje como *muy picante* 🔥"
                elif mensaje.picante >= Constantes.PartidaClasica.VALOR_PICANTE_MEDIO:
                    msg += u"\n\nSe ha indicado el mensaje como *picante* 🌶"
                elif mensaje.picante > 0:
                    msg += u"\n\nSe ha indicado el mensaje como *ligeramente picante* ♨️"

                keyboard = Teclados.revisar_mensajes_valor(mensaje.id)
            else:

                msg = "Parece que ya has revisado todos los mensajes. Vuelve a intentarlo más tarde, o añade tus pro" \
                      "pios mensajes."
                keyboard = Teclados.solo_menu_principal()

        else:

            mensaje1 = dame_mensaje_a_revisar()
            mensaje2 = dame_mensaje_a_revisar()
            antiloop = 0

            while (mensaje1.picante == 0 or mensaje1 == mensaje2) and antiloop < 100:
                mensaje1 = dame_mensaje_a_revisar()
                antiloop += 1

            while (mensaje2.picante == 0 or mensaje1 == mensaje2) and antiloop < 100:
                mensaje2 = dame_mensaje_a_revisar()
                antiloop += 1

            if antiloop < 100:
                if mensaje1.tipo == "normal":
                    msg1 = mensaje1.text
                else:
                    msg1 = u"%s\"\n\"%s" % (mensaje1.text0, mensaje1.text1)

                if mensaje2.tipo == "normal":
                    msg2 = mensaje2.text
                else:
                    msg2 = u"%s\"\n\"%s" % (mensaje2.text0, mensaje2.text1)

                msg = u"*Escoje de los dos mensajes el más picante. Primer mensaje:*" \
                      u"\n\"%s\"\n\n*Segundo mensaje:*\n\"%s\"" % (msg1, msg2)
                keyboard = Teclados.revisar_mensajes_picante(mensaje1.id, mensaje2.id)
            else:
                msg = "Parece que ya has revisado todos los mensajes. Vuelve a intentarlo más tarde, o añade tus pro" \
                      "pios mensajes."
                keyboard = Teclados.solo_menu_principal()

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def revisar_actualizar_valor(self, bot, update):

        data = update.callback_query.data
        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        msgID = data.split("-")[1]
        mensaje = MensajesEnRevision.get_message(msgID)

        if mensaje and mensaje.hecho_por != usuario.id:
            if re.match(r"revisar_valor_1down", data):
                mensaje.puntos += (Puntos((-1, -0.4)) * (usuario.reputacion / Constantes.Usuarios.REPUTACION_INICIAL))
                mensaje.en_contra.append(usuario.id)
            elif re.match(r"revisar_valor_skip", data):
                mensaje.skipped.append(usuario.id)
            elif re.match(r"revisar_valor_1up", data):
                mensaje.puntos += (Puntos((1, 0.1)) * (usuario.reputacion / Constantes.Usuarios.REPUTACION_INICIAL))
                mensaje.a_favor.append(usuario.id)
            elif re.match(r"revisar_valor_2up", data):
                mensaje.puntos += (Puntos((2, 0.2)) * (usuario.reputacion / Constantes.Usuarios.REPUTACION_INICIAL))
                mensaje.a_favor.append(usuario.id)
            elif re.match(r"revisar_rev", data):
                mensaje.puntos += (Puntos((-0.5, -1)) * (usuario.reputacion / Constantes.Usuarios.REPUTACION_INICIAL))
                mensaje.skipped.append(usuario.id)

            MensajesEnRevision.comprobar_aptitud(mensaje)
        elif mensaje:
            if re.match(r"revisar_valor_1down", data):
                mensaje.en_contra.append(usuario.id)
            elif re.match(r"revisar_valor_skip", data):
                mensaje.skipped.append(usuario.id)
            elif re.match(r"revisar_valor_1up", data):
                mensaje.a_favor.append(usuario.id)
            elif re.match(r"revisar_valor_2up", data):
                mensaje.a_favor.append(usuario.id)
            elif re.match(r"revisar_rev", data):
                mensaje.skipped.append(usuario.id)

        self.revisar_mensajes(bot, update)

    def revisar_actualizar_picante(self, bot, update):

        data = update.callback_query.data
        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        if not data == "revisar_picante_pass":
            msg1ID = data.split("-")[1]
            msg2ID = data.split("-")[2]
            mensaje1 = MensajesEnRevision.get_message(msg1ID)
            mensaje2 = MensajesEnRevision.get_message(msg2ID)

            if not mensaje2:
                mensaje2 = MensajesClasica.get_message(msg2ID)

            if mensaje1 and mensaje2:

                if re.match(r"revisar_picante_1", data):
                    factor = (mensaje2.picante / mensaje1.picante)
                    if factor > ((mensaje1.picante + mensaje2.picante)/2):
                        factor = (mensaje1.picante + mensaje2.picante)/2
                    mensaje1.picante += factor
                    mensaje2.picante -= factor
                else:
                    factor = (mensaje1.picante / mensaje2.picante)
                    if factor > ((mensaje1.picante + mensaje2.picante)/2):
                        factor = (mensaje1.picante + mensaje2.picante)/2
                    mensaje2.picante += factor
                    mensaje1.picante -= factor

                if mensaje1.picante < 1:
                    mensaje1.picante = 1
                if mensaje2.picante < 1:
                    mensaje2.picante = 1

        self.revisar_mensajes(bot, update)

    def add_message(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        usuario.editando_mensaje = None

        if usuario.reputacion >= Constantes.Usuarios.ACESO_A_ADD_MESSAGE:
            msg, keyboard = Menus.menu_add_message()
        else:
            msg = "Lo sentimos, pero ahora mismo no tienes acceso a esta función. Prueba a revisar unos mensajes y" \
                  " vuelve más tarde."
            keyboard = Teclados.solo_menu_principal()

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def add_normal(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        msg_dicc = {"id": uuid.uuid4().get_hex()[:8],
                    "tipo": "normal",
                    "text": None,
                    "picante": 0,
                    "hecho_por": usuario.id,
                    "revisar": {"a_favor": [],
                                "en_contra": [],
                                "skipped": [],
                                "puntos": (0, 0)}}

        usuario.editando_mensaje = MensajeEnRevision(msg_dicc)

        msg = "*Añadiendo mensaje normal.* Ahora mandame el mensaje.\n\n*CONSEJOS:*\n-Para poner *nombres aleatorios* escribe *nombre1* o *{1}* para" \
              " el primero y *nombre2* o *{2}* para el segundo.\n-Rodea con asteriscos lo que quieres que salga en *" \
              "negrita*.\n-Rodea con barras bajas lo que quieres que salga en _cursiva._"
        keyboard = Teclados.menu_add_cancelar()

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

        return 0

    def add_RI(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        msg_dicc = {"id": uuid.uuid4().get_hex()[:8],
                    "tipo": "RI",
                    "text0": None,
                    "text1": None,
                    "picante": 0,
                    "hecho_por": usuario.id,
                    "revisar": {"a_favor": [],
                                "en_contra": [],
                                "skipped": [],
                                "puntos": (0, 0)}}

        usuario.editando_mensaje = MensajeEnRevision(msg_dicc)

        msg = "*Añadiendo mensaje RI.* Ahora mandame el primer mensaje.\n\n*CONSEJOS:*\n-Para poner *nombres aleatorios* escribe *nombre1* o *{1}* para" \
              " el primero y *nombre2* o *{2}* para el segundo.\n-Rodea con asteriscos lo que quieres que salga en *" \
              "negrita*.\n-Rodea con barras bajas lo que quieres que salga en _cursiva._"
        keyboard = Teclados.menu_add_cancelar()

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

        return 1

    def add_RNI(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        msg_dicc = {"id": uuid.uuid4().get_hex()[:8],
                    "tipo": "RNI",
                    "text0": None,
                    "text1": None,
                    "picante": 0,
                    "hecho_por": usuario.id,
                    "revisar": {"a_favor": [],
                                "en_contra": [],
                                "skipped": [],
                                "puntos": (0, 0)}}

        usuario.editando_mensaje = MensajeEnRevision(msg_dicc)

        msg = "*Añadiendo mensaje RNI.* Ahora mandame el primer mensaje.\n\n*CONSEJOS:*\n-Para poner *nombres aleatorios* escribe *nombre1* o *{1}* para" \
              " el primero y *nombre2* o *{2}* para el segundo.\n-Rodea con asteriscos lo que quieres que salga en *" \
              "negrita*.\n-Rodea con barras bajas lo que quieres que salga en _cursiva._"
        keyboard = Teclados.menu_add_cancelar()

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

        return 1

    def add_picante(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        data = update.callback_query.data
        
        if data == "pic_mas_picante":
            if usuario.editando_mensaje.picante == Constantes.PartidaClasica.VALOR_PICANTE_MEDIO:
                usuario.editando_mensaje.picante = Constantes.PartidaClasica.VALOR_PICANTE_ALTO
            elif usuario.editando_mensaje.picante == Constantes.PartidaClasica.VALOR_PICANTE_BAJO:
                usuario.editando_mensaje.picante = Constantes.PartidaClasica.VALOR_PICANTE_MEDIO
            elif usuario.editando_mensaje.picante == 0:
                usuario.editando_mensaje.picante = Constantes.PartidaClasica.VALOR_PICANTE_BAJO
                
        elif data == "pic_menos_picante":
            if usuario.editando_mensaje.picante == Constantes.PartidaClasica.VALOR_PICANTE_ALTO:
                usuario.editando_mensaje.picante = Constantes.PartidaClasica.VALOR_PICANTE_MEDIO
            elif usuario.editando_mensaje.picante == Constantes.PartidaClasica.VALOR_PICANTE_MEDIO:
                usuario.editando_mensaje.picante = Constantes.PartidaClasica.VALOR_PICANTE_BAJO
            elif usuario.editando_mensaje.picante == Constantes.PartidaClasica.VALOR_PICANTE_BAJO:
                usuario.editando_mensaje.picante = 0

        elif data == "pic_done":

            usuario.reputacion -= 10
            MensajesEnRevision.list.append(usuario.editando_mensaje)
            self.add_message(bot, update)

            return ConversationHandler.END

        if usuario.editando_mensaje.tipo == "normal":
            msg, keyboard = Menus.menu_add_picante(text0=usuario.editando_mensaje.text,
                                                   picante=usuario.editando_mensaje.picante)
        else:
            msg, keyboard = Menus.menu_add_picante(text0=usuario.editando_mensaje.text0,
                                                   text1=usuario.editando_mensaje.text1,
                                                   picante=usuario.editando_mensaje.picante)

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

        return 3

    def add_text(self, bot, update):

        usuario = Usuarios.get_user(update.message.from_user.id)

        usuario.editando_mensaje.text = update.message.text

        msg, keyboard = Menus.menu_add_picante(text0=usuario.editando_mensaje.text,
                                               picante=usuario.editando_mensaje.picante)

        update.message.reply_text(text=msg,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.MARKDOWN)

        return 3

    def add_text0(self, bot, update):

        usuario = Usuarios.get_user(update.message.from_user.id)

        usuario.editando_mensaje.text0 = update.message.text

        msg = "Ahora mandame el segundo mensaje. Primer mensaje:\n\"%s\"\n\n*CONSEJOS:*\n-Para poner *nombres aleatorios* escribe *nombre1* o *{1}* para" \
              " el primero y *nombre2* o *{2}* para el segundo.\n-Rodea con asteriscos lo que quieres que salga en *" \
              "negrita*.\n-Rodea con barras bajas lo que quieres que salga en _cursiva._" % usuario.editando_mensaje.text0
        keyboard = Teclados.menu_add_cancelar()

        update.message.reply_text(text=msg,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.MARKDOWN)

        return 2

    def add_text1(self, bot, update):

        usuario = Usuarios.get_user(update.message.from_user.id)

        usuario.editando_mensaje.text1 = update.message.text

        msg, keyboard = Menus.menu_add_picante(text0=usuario.editando_mensaje.text0,
                                               text1=usuario.editando_mensaje.text1,
                                               picante=usuario.editando_mensaje.picante)

        update.message.reply_text(text=msg,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.MARKDOWN)

        return 3

    # MENÚ DE PARTIDA CLÁSICA
    def menu_partidaClasica(self, bot, update):

        update.callback_query.answer()

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        menu = Menus.menu_partidaClasica(usuario.ajustes.picante, usuario.ajustes.emparejador, usuario.ultimos_jugadores)
        msg = menu[0]
        keyboard = menu[1]

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def partida_clasica_jugadores(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        dicc_fac_picante = {0: Constantes.PartidaClasica.FACTOR_PICANTE_NO_PICANTE,
                            1: Constantes.PartidaClasica.FACTOR_PICANTE_BAJO,
                            2: Constantes.PartidaClasica.FACTOR_PICANTE_MEDIO,
                            3: Constantes.PartidaClasica.FACTOR_PICANTE_ALTO}

        if usuario.ajustes.emparejador:

            usuario.partida = PartidaClasicaEmparejador(usuario,
                                                        factor_picante=dicc_fac_picante[usuario.ajustes.picante])
            usuario.ultimos_jugadores = []
        else:

            usuario.partida = PartidaClasica(usuario,
                                             factor_picante=dicc_fac_picante[usuario.ajustes.picante])
            usuario.ultimos_jugadores = []

        usuario.partida.inciar_mensajes()
        usuario.partida.iniciar_valor_picante()

        msg, keyboard = Menus.menu_add_player(usuario.partida.jugadores)

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

        return 0

    def partida_clasica_ultimos_jugadores(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        dicc_fac_picante = {0:Constantes.PartidaClasica.FACTOR_PICANTE_NO_PICANTE,
                            1:Constantes.PartidaClasica.FACTOR_PICANTE_BAJO,
                            2:Constantes.PartidaClasica.FACTOR_PICANTE_MEDIO,
                            3:Constantes.PartidaClasica.FACTOR_PICANTE_ALTO}

        if usuario.ajustes.emparejador:

            usuario.partida = PartidaClasicaEmparejador(usuario,
                                                        factor_picante=dicc_fac_picante[usuario.ajustes.picante],
                                                        jugadores=usuario.ultimos_jugadores)
            usuario.partida.inciar_mensajes()
            usuario.partida.iniciar_valor_picante()
            usuario.partida.iniciar_cola()
            Accion = usuario.partida.acciones_pendientes[-1]

            msg, keyboard = Menus.menu_emparejador(Accion)

            bot.edit_message_text(text=msg,
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.MARKDOWN)

            return 1
        else:

            msg = "Iniciando partida..."

            bot.edit_message_text(text=msg,
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  parse_mode=ParseMode.MARKDOWN)

            usuario.partida = PartidaClasica(usuario,
                                             factor_picante=dicc_fac_picante[usuario.ajustes.picante],
                                             jugadores=usuario.ultimos_jugadores)

            usuario.partida.inciar_mensajes()
            usuario.partida.iniciar_valor_picante()

            self.next_mesagge(bot, update)

            return ConversationHandler.END

    def partida_clasica_menos_picante(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        too_cold_messages = ["buah.",
                            "no os veo muy animados",
                            "que aburiiidoooos!",
                            "💤💤💤💤",
                            "lo que pasa es que os falta alcohol en el cuerpo",
                            "¿teneis todos pareja o qué?",
                            "Nunca me habían pedido algo así...",
                            "Menos picante que nada no puede ser, déjalo ya",
                            "Poco más y morís de hipotermia",
                            "¿tienéis calefacción en casa?",
                            "¿no deberíais estar con vuestros papis?"]

        if usuario.ajustes.picante > 0:
            usuario.ajustes.picante -= 1
            self.menu_partidaClasica(bot, update)
        else:
            update.callback_query.answer(too_cold_messages[random.randint(0, 10)])

    def partida_clasica_picante_info(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        pic_dic = {0:"Nivel de picante: ❄ nada picante️",
                   1:"Nivel de picante: ♨️ ligeramente picante",
                   2:"Nivel de picante: 🌶 picante",
                   3:"Nivel de picante: 🔥 muy picante"}

        update.callback_query.answer(pic_dic[usuario.ajustes.picante])

    def partida_clasica_mas_picante(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        too_hot_messages = ["wow, so hot",
                            "🔥🔥🔥",
                            "Llamad a los bomberos! 🚒💦",
                            "Lo vais a dar todo esta noche eh?",
                            "Increíblemente calientes",
                            "error 1503: jugadores demasiado calientes",
                            "¿necesitais condón o cama?",
                            "El calor del sol acaba de quedar en ridículo",
                            "Lo sentimos, Piloco no soporta tan altas temperaturas",
                            "Deja de intentarlo, no puedes ponerlo más caliente",
                            "Tal vez deberíais probar a desnudaros",
                            "Piloco no está capacitado para bajaros los pantalones"]

        if usuario.ajustes.picante < 3:
            usuario.ajustes.picante += 1
            self.menu_partidaClasica(bot, update)
        else:
            update.callback_query.answer(too_hot_messages[random.randint(0,11)])

    def partida_clasica_emparejador(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        if usuario.ajustes.emparejador:
            usuario.ajustes.emparejador = False
        else:
            usuario.ajustes.emparejador = True

        self.menu_partidaClasica(bot, update)

    def partida_clasica_add_player(self, bot, update):

        usuario = Usuarios.get_user(update.message.from_user.id)

        usuario.partida.add_player(update.message.text)
        usuario.add_player(update.message.text)

        # TODO: no debería soportar mensajes largos y debería comprobar si los jugadores ya exisiten.
        # Esto último debería comprobarse dentro el método add_player y que este devuelva 1 o 0.
        # Al mismo tiempo, las excecpiónes deberían añadirse como fallbacks al ConversationHandler.

        msg, keyboard = Menus.menu_add_player(usuario.partida.jugadores)

        bot.send_message(text=msg,
                         chat_id=update.message.from_user.id,
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         parse_mode=ParseMode.MARKDOWN)

        msg = u"👥*AÑADIR JUGADORES*\n\nSe ha añadido a %s" %update.message.text.capitalize()
        keyboard = [[]]

        bot.edit_message_text(text=msg,
                              chat_id=update.message.chat_id,
                              message_id=update.message.message_id - 1,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

        return 0

    # EN PARTIDA
    def next_mesagge(self, bot, update):
        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        msg = usuario.partida.dame_mensaje()

        keyboard = Teclados.menu_mensaje()

        bot.send_message(text=msg,
                         chat_id=update.callback_query.from_user.id,
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         parse_mode=ParseMode.MARKDOWN)

        keyboard = [[]]

        bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    def start_vote_partida_clasica(self, bot, update):

        keyboard = Teclados.menu_votar_partida()

        bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    def partida_clasica_vote_up(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        usuario.partida.last_message.puntuacion += usuario.reputacion / Constantes.Usuarios.REPUTACION_INICIAL

        self.next_mesagge(bot, update)

    def partida_clasica_vote_down(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        usuario.partida.last_message.puntuacion -= usuario.reputacion / Constantes.Usuarios.REPUTACION_INICIAL

        self.next_mesagge(bot, update)

        # TODO: hay que comrobar si el mensaje se tiene que largar a narnia, teniendo en cuenta la posibilidad de que
        # este mismo mensaje esté en otra partida y esté siendo votado.
        # TODO: debe soportar la posibilidad de que el usuario no esté en partida
        # TODO: tiene que soportar mensajes tipo RNI y RI

    def ajustes_partida_clasica(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        emparejador = usuario.partida.emparejador

        msg = Menus.menu_ajustes_partida_clasica(emparejador)[0]
        keyboard = Menus.menu_ajustes_partida_clasica(emparejador)[1]

        bot.send_message(text=msg,
                         chat_id=update.callback_query.message.chat_id,
                         reply_markup=InlineKeyboardMarkup(keyboard),
                         parse_mode=ParseMode.MARKDOWN)

        keyboard = [[]]

        bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    def partida_clasica_volver(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        msg = usuario.partida.dame_mensaje()

        keyboard = Teclados.menu_mensaje()

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

    def partida_clasica_salir(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        usuario.partida = None

        self.menu_principal(bot, update)

    def ajustes_mas_picante(self, bot, update):  # TODO: si factor == 0? + partidas con emparejador bien ploes

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        fac_picante = [Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO,
                       Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO,
                       Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO]
        val_picante = [Constantes.PartidaClasica.FACTOR_PICANTE_BAJO,
                       Constantes.PartidaClasica.FACTOR_PICANTE_MEDIO,
                       Constantes.PartidaClasica.FACTOR_PICANTE_ALTO]

        actual = fac_picante.index(usuario.partida.factor_picante)

        if actual < 2:
            nuevo = actual + 1
        else:
            nuevo = actual

        usuario.partida.factor_picante = fac_picante[nuevo]

        if nuevo != actual:
            usuario.partida.valor_picante *= 2

        if usuario.partida.valor_picante == 0:
            usuario.partida.valor_picante = val_picante[nuevo]

        update.callback_query.answer("Nivel de picante aumentado")

    def ajustes_menos_picante(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        fac_picante = [Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO,
                       Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO,
                       Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO]

        actual = fac_picante.index(usuario.partida.factor_picante)

        if actual > 0:
            nuevo = actual - 1
        else:
            nuevo = actual

        usuario.partida.factor_picante = fac_picante[nuevo]
        usuario.partida.valor_picante /= 2

        update.callback_query.answer("Nivel de picante reducido")

    def partida_clasica_iniciar(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)

        if len(usuario.partida.jugadores) > 1:
            if usuario.partida.emparejador:
                usuario.partida.iniciar_cola()
                Accion = usuario.partida.acciones_pendientes[-1]

                msg, keyboard = Menus.menu_emparejador(Accion)

                bot.edit_message_text(text=msg,
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=InlineKeyboardMarkup(keyboard),
                                      parse_mode=ParseMode.MARKDOWN)
                return 1
            else:
                msg = "Iniciando partida..."
                keyboard = [[]]

                bot.edit_message_text(text=msg,
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=InlineKeyboardMarkup(keyboard),
                                      parse_mode=ParseMode.MARKDOWN)

                self.next_mesagge(bot, update)

                return ConversationHandler.END
        else:
            msg = "👥*AÑADIR JUGADORES*\n\nTienes que proporcionarme al menos dos jugadores.\n\n" \
                  "Ahora envíame uno por uno los nombres de los jugadores."
            keyboard = [[]]

            bot.edit_message_text(text=msg,
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode=ParseMode.MARKDOWN)
            return 0

    def emparejador_encuesta(self, bot, update):

        usuario = Usuarios.get_user(update.callback_query.from_user.id)
        UltimaAccion = usuario.partida.acciones_pendientes.pop(-1)
        Accion = usuario.partida.acciones_pendientes[-1]

        if UltimaAccion.accion == ColaEmparejador.ENCUESTA:

            potencia = int(update.callback_query.data.split("-")[1])

            UltimaAccion.nodo1.elegir(UltimaAccion.nodo2, potencia)

            if potencia == 0:
                UltimaAccion.nodo1.descarto()

        msg, keyboard = Menus.menu_emparejador(Accion)

        bot.edit_message_text(text=msg,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN)

        if Accion.accion == ColaEmparejador.TERMINAR_ENCUESTAS:

            usuario.partida.inicializar_toda_relacion()

            self.next_mesagge(bot, update)

            return ConversationHandler.END

        return 1

HandlersPiloco = HandlersPiloco()


class Conversations:

    add_players = ConversationHandler(entry_points=[CallbackQueryHandler(HandlersPiloco.partida_clasica_jugadores,
                                                                         pattern="^mpc_start$"),

                                                    CallbackQueryHandler(
                                                        HandlersPiloco.partida_clasica_ultimos_jugadores,
                                                        pattern="^mpc_last_players$")],

                                      states={0:[MessageHandler(Filters.text, HandlersPiloco.partida_clasica_add_player),
                                                 CallbackQueryHandler(HandlersPiloco.partida_clasica_iniciar, pattern="^done_players")],
                                              1:[CallbackQueryHandler(HandlersPiloco.emparejador_encuesta,
                                                                      pattern="^emp")]},

                                      fallbacks=[CommandHandler('restart', HandlersPiloco.restart_bot)],

                                      allow_reentry=True)

    add_message = ConversationHandler(entry_points=[CallbackQueryHandler(HandlersPiloco.add_normal, pattern="^newMessage_normal$"),
                                                    CallbackQueryHandler(HandlersPiloco.add_RI, pattern="^newMessage_RI$"),
                                                    CallbackQueryHandler(HandlersPiloco.add_RNI, pattern="^newMessage_RNI$")],

                                      states={0: [MessageHandler(Filters.text, HandlersPiloco.add_text)],
                                              1: [MessageHandler(Filters.text, HandlersPiloco.add_text0)],
                                              2: [MessageHandler(Filters.text, HandlersPiloco.add_text1)],
                                              3: [CallbackQueryHandler(HandlersPiloco.add_picante, pattern="^pic_")]},

                                      fallbacks=[CommandHandler('restart', HandlersPiloco.restart_bot),
                                                 CallbackQueryHandler(HandlersPiloco.add_message, pattern="^ms_new$")],

                                      allow_reentry=True)
