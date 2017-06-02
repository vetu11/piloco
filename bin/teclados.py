# coding=utf-8

from telegram import InlineKeyboardButton
from .partida import ColaEmparejador
from .constantes import Constantes

class Teclados:

    """Todos los teclados que necesita Piloco"""

    # GENERAL
    def menu_principal(self):

        keyboard = [[InlineKeyboardButton("▶️ Nueva partida", callback_data="mp_newGame")],

                    [InlineKeyboardButton("✉ Añadir/Revisar mensajes", callback_data="mp_mensajes")],

                    [InlineKeyboardButton("⚙️", callback_data="mp_ajustes"),
                     InlineKeyboardButton("ℹ️", callback_data="mp_info"),
                     InlineKeyboardButton("🆘", callback_data="mp_help")]]
        return keyboard

    def menu_partidaClasica(self, picante=0, emparejador=False, last_players=False):

        pic_dicc = {0:"❄️", 1:"♨️", 2:"🌶", 3:"🔥"}
        emp_dicc = {0:"❎", 1:"✅"}

        keyboard = [[InlineKeyboardButton("▶️ Iniciar partida", callback_data="mpc_start")]]

        if last_players:

            keyboard.append([InlineKeyboardButton("👥 ▶ Jugar con los últimos jugadores️", callback_data="mpc_last_players")])

        keyboard.append([InlineKeyboardButton("❄ ⬅️️️", callback_data="mpc_menos_picante"),
                         InlineKeyboardButton("%s" %pic_dicc[picante], callback_data="mpc_picante_info"),
                         InlineKeyboardButton("➡️ 🔥️", callback_data="mpc_mas_picante")])
        keyboard.append([InlineKeyboardButton("Emparejador %s" %emp_dicc[emparejador], callback_data="mpc_emparejador")])
        keyboard.append([InlineKeyboardButton("🏠 Volver", callback_data="mp")])

        # TODO: last_players recibe una lista. ¿esto es optimizable?

        return keyboard

    def menu_mensajes(self):

        keyboard = [[InlineKeyboardButton("📨 Añadir mensajes", callback_data="ms_new")],
                    [InlineKeyboardButton("🔍 Revisar mensajes", callback_data="ms_rev")],
                    [InlineKeyboardButton("📝 Corregir mensajes", callback_data="ms_crg")],
                    [InlineKeyboardButton("🏠 Volver", callback_data="mp")]]
        return keyboard

    def menu_info(self):

        keyboard = [[InlineKeyboardButton("📢 Canal", url="t.me/Piloco")],
                    [InlineKeyboardButton("💬 Habla con nosotros", url="t.me/PilocoSupportbot")],
                    [InlineKeyboardButton("🏠 Volver", callback_data="mp")]]
        return keyboard

    def solo_menu_principal(self):

        keyboard = [[InlineKeyboardButton("🏠 Volver", callback_data="mp")]]
        return keyboard

    # MENSAJES
    def revisar_mensajes_valor(self, msgID):

        keyboard = [[InlineKeyboardButton("1️⃣⬇️", callback_data="revisar_valor_1down-%s" % msgID),
                     InlineKeyboardButton("0️⃣", callback_data="revisar_valor_skip-%s" % msgID),
                     InlineKeyboardButton("1️⃣⬆️", callback_data="revisar_valor_1up-%s" % msgID),
                     InlineKeyboardButton("2️⃣⬆️", callback_data="revisar_valor_2up-%s" % msgID)],

                    [InlineKeyboardButton("🔙 enviar a corregir️", callback_data="revisar_rev-%s" % msgID)],

                    [InlineKeyboardButton("🏠 Volver", callback_data="mp")]]

        return keyboard

    def revisar_mensajes_picante(self, msg1ID, msg2ID):

        keyboard = [[InlineKeyboardButton("El primero es más picante",
                                          callback_data="revisar_picante_1-%s-%s" % (msg1ID, msg2ID))],

                    [InlineKeyboardButton("El segundo es más picante",
                                          callback_data="revisar_picante_2-%s-%s" % (msg1ID, msg2ID))],

                    [InlineKeyboardButton("Los dos son igual de picantes", callback_data="revisar_picante_pass")],

                    [InlineKeyboardButton("🏠 Volver", callback_data="mp")]]
        return keyboard

    def menu_add_message(self):

        keyboard = [[InlineKeyboardButton("normal 💬", callback_data="newMessage_normal"),
                     InlineKeyboardButton("RI 💬💬", callback_data="newMessage_RI"),
                     InlineKeyboardButton("RNI 💬🕐💬", callback_data="newMessage_RNI")],

                    [InlineKeyboardButton("AYUDA POFABÓ 🆘", url="telegra.ph/Okay-03-12")],

                    [InlineKeyboardButton("🏠 Volver", callback_data="mp")]]
        return keyboard

    def menu_add_cancelar(self):
        keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data="ms_new")]]
        return keyboard

    def menu_add_picante(self, picante):
        pic_dicc = {0: "❄️",
                    Constantes.PartidaClasica.VALOR_PICANTE_BAJO: "♨️",
                    Constantes.PartidaClasica.VALOR_PICANTE_MEDIO: "🌶",
                    Constantes.PartidaClasica.VALOR_PICANTE_ALTO: "🔥"}

        keyboard = [[InlineKeyboardButton("⬅️❄️", callback_data="pic_menos_picante"),
                     InlineKeyboardButton("%s" % pic_dicc[picante], callback_data="nanainanull"),
                     InlineKeyboardButton("🔥➡️", callback_data="pic_mas_picante")],

                    [InlineKeyboardButton("❌ Cancelar", callback_data="ms_new"),
                     InlineKeyboardButton("Hecho 👌", callback_data="pic_done")]]
        return keyboard

    # EN PARTIDA
    def menu_ecuesta_emparejador(self, descartes_restantes):

        if descartes_restantes:
            keyboard = [[InlineKeyboardButton("❌", callback_data="emp-0"),
                         InlineKeyboardButton("1️⃣", callback_data="emp-1"),
                         InlineKeyboardButton("2️⃣", callback_data="emp-2"),
                         InlineKeyboardButton("3️⃣", callback_data="emp-3"),
                         InlineKeyboardButton("4️⃣", callback_data="emp-4"),
                         InlineKeyboardButton("5️⃣", callback_data="emp-5")]]
        else:
            keyboard = [[InlineKeyboardButton("1️⃣", callback_data="emp-1"),
                         InlineKeyboardButton("2️⃣", callback_data="emp-2"),
                         InlineKeyboardButton("3️⃣", callback_data="emp-3"),
                         InlineKeyboardButton("4️⃣", callback_data="emp-4"),
                         InlineKeyboardButton("5️⃣", callback_data="emp-5")]]

        return keyboard

    def menu_mensaje(self, botones_picante=False):  # TODO: comprobar si el mensaje es picante para añadir los botones de "demasiado caliente"

        keyboard = [[InlineKeyboardButton("⚙️ / 🚪", callback_data="pc_ajustes"),
                     InlineKeyboardButton("⬇️🌟⬆️", callback_data="pc_votar"),
                     InlineKeyboardButton("✉️⏭", callback_data="pc_next")]]
        return keyboard

    def menu_votar_partida(self):

        keyboard = [[InlineKeyboardButton("⬇️", callback_data="pc_vote_down"),
                     InlineKeyboardButton("0️⃣", callback_data="pc_next"),
                     InlineKeyboardButton("⬆️", callback_data="pc_vote_up")]]
        return keyboard

    def menu_ajustes_partida_clasica(self, emparejador=False):

        keyboard = []
        if not emparejador:
            keyboard.append([InlineKeyboardButton("❌👤Eliminar jugador", callback_data="apc_delete_player"),
                             InlineKeyboardButton("Añadir jugador➕👤", callback_data="apc_add_player")])

        keyboard.append([InlineKeyboardButton("❄️⬅️Menos picante", callback_data="apc_menos_picante"),
                         InlineKeyboardButton("Más picante➡️🔥", callback_data="apc_mas_picante")])

        keyboard.append([InlineKeyboardButton("🚪🏃‍♀️Salir", callback_data="apc_salir"),
                         InlineKeyboardButton("Volver⏭", callback_data="apc_volver")])
        return keyboard

Teclados = Teclados()


class Menus():

    """Todos los menús que necesita Piloco"""

    def menu_principal(self):

        msg = "🏠*MENÚ PRINCIPAL\n\n¡Bienvenido a Piloco!*\n\n¿listas para emborracharse?\nUsa los botones para navegar por los menús."

        keyboard = Teclados.menu_principal()
        return msg,keyboard

    def menu_partidaClasica(self, picante, emparejador, last_players):

        msg = "▶️*PARTIDA CLÁSICA*\n\nConfigura tu partida y pulsa iniciar partida."

        keyboard = Teclados.menu_partidaClasica(picante, emparejador, last_players)
        return [msg, keyboard]

    def menu_mensajes(self):

        msg = "✉️*MENSAJES*\n\nDesde aquí puedes añadir, revisar o corregir mensajes que más tarde aparecerán en el j" \
              "uego." # TODO: cambiar el texto para que se entienda mejor en qué consiste revisar mensajes

        keyboard = Teclados.menu_mensajes()
        return [msg, keyboard]

    def menu_info(self, usuario ):

        msg = "ℹ️*INFORMACIÓN*\n\n▪️[Canal oficial de Piloco](t.me/Piloco), *noticias y otros.*\n▪️¿Tienes *ideas nuevas" \
              "* para Piloco, o *alguna duda*? Habla con [nosotros](@PilocoSupportbot)\n▪️Tienes *%s puntos de reputa" \
              "ción* [¿qué es eso?](telegra.ph/reputación-y-recompensas-05-27)\n\n" \
              "v1.0-alpha21" % int(usuario.reputacion)

        keyboard = Teclados.menu_info()
        return msg, keyboard

    def menu_ajustes_partida_clasica(self, emparejador=False):

        msg = "⚙️*AJUSTES DE PARTIDA CLASICA*\n\nCambia los ajustes de partida desde aquí."
        keyboard = Teclados.menu_ajustes_partida_clasica(emparejador)
        return [msg, keyboard]

    def menu_add_player(self, lista_jugadores):
        """La lista de jugadores se proporciona como objetos"""

        jugadores = u""

        for jugador in lista_jugadores:
            nombre = jugador.nombre.capitalize()
            jugadores = jugadores.replace("{1}", "{2}").replace("{0}", "{1}")
            jugadores += u"%s{0}"%nombre

        jugadores = jugadores.format("", " y ", ", ")

        msg = u"👥*AÑADIR JUGADORES*\n\nAhora envíame uno por uno los nombres de los jugadores.\n\n" \
              u"*Jugadores actuales:* %s" %jugadores
        keyboard = [[InlineKeyboardButton("Iniciar partida", callback_data="done_players")]]

        return msg, keyboard

    def menu_emparejador(self, Accion):

        if Accion.accion == ColaEmparejador.PEDIR_MOVIL:

            msg = u"Antes de empezar, *%s* tiene que responder unas preguntas... *Pasadle el móvil*" % Accion.nodo1.nombre
            keyboard = [[InlineKeyboardButton("Iniciar preguntas", callback_data="emp_empezar_encuesta")]]

        elif Accion.accion == ColaEmparejador.ENCUESTA:

            descartes_restantes = Accion.nodo1.descartes_restantes

            msg = u"*%s*, ¿cómo ves a *%s* esta noche?\n\nTienes *%d* descartes restantes." \
                  % (Accion.nodo1.nombre, Accion.nodo2.nombre, Accion.nodo1.descartes_restantes)
            keyboard = Teclados.menu_ecuesta_emparejador(descartes_restantes)

        else:

            msg = "Iniciando partida..."
            keyboard = [[]]

        return msg, keyboard

    def menu_add_message(self):
        msg = "📨*AÑADIR MENSAJES*\n\nDesde este menú puedes añadir mensajes que más tarde aparecerán en el juego\n\n" \
              "Elige el tipo de mensaje que quieres añadir.\nLos mensajes *normales* tienen un solo mensaje 💬\nLos " \
              "mensajes tipo *RI* tienen dos mensajes, el segundo aparecerá inmediatamente después del primero 💬💬\n" \
              "Los mensajes tipo *RNI* tienen dos mensajes, y el segundo aparecerá más tarde que el primero 💬🕑💬"
        keyboard = Teclados.menu_add_message()
        return msg, keyboard

    def menu_add_picante(self, text0, text1=None, picante=0):

        if text1:
            msg = u"Tu mensaje:\n\n\"%s\"\n\"%s\"\n\nNivel de picante: " % (text0, text1)
        else:
            msg = u"Tu mensaje:\n\n\"%s\"\n\nNivel de picante: " % (text0)

        if picante >= Constantes.PartidaClasica.VALOR_PICANTE_ALTO:
            msg += u"*muy picante* 🔥"
        elif picante >= Constantes.PartidaClasica.VALOR_PICANTE_MEDIO:
            msg += u"*picante* 🌶"
        elif picante > 0:
            msg += u"*ligeramente picante* ♨️"
        else:
            msg += u"*nada picante* ❄️"

        keyboard = Teclados.menu_add_picante(picante)
        return msg, keyboard

Menus = Menus()
