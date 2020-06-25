# coding=utf-8

from telegram import InlineKeyboardButton
from .partida import ColaEmparejador
from .constantes import Constantes


class Teclados:

    """Todos los teclados que necesita Piloco"""

    # GENERAL
    
    def menu_principal(self, usuario):

        n_msg = usuario.mensajes_sin_votar()
        if n_msg:
            n_msg = " - 🆕%s🆕" % n_msg
        else:
            n_msg = ""

        keyboard = [[InlineKeyboardButton("▶️ Nueva partida", callback_data="mp_newGame")],

                    [InlineKeyboardButton("✉ Añadir/Votar mensajes%s"  % n_msg, callback_data="mp_mensajes")],

                    [InlineKeyboardButton("ℹ️", callback_data="mp_info"),
                     InlineKeyboardButton("▫️", callback_data="mp_donate")]]
        return keyboard
    
    
    def menu_partidaClasica(self, picante=0, emparejador=False, last_players=False):

        pic_dicc = {0:"❄️", 1:"♨️", 2:"🌶", 3:"🔥"}
        emp_dicc = {0:"❎️", 1:"✅"}

        keyboard = [[InlineKeyboardButton("▶️ Iniciar partida", callback_data="mpc_start")]]

        if last_players:

            keyboard.append([InlineKeyboardButton("👥 ▶ Jugar con los últimos jugadores️", callback_data="mpc_last_players")])

        keyboard.append([InlineKeyboardButton("❄ ⬅️️️", callback_data="mpc_menos_picante"),
                         InlineKeyboardButton("%s" %pic_dicc[picante], callback_data="mpc_picante_info"),
                         InlineKeyboardButton("➡️ 🔥️", callback_data="mpc_mas_picante")])
        keyboard.append([InlineKeyboardButton("Emparejador %s" %emp_dicc[emparejador], callback_data="mpc_emparejador")])
        keyboard.append([InlineKeyboardButton("🏠 Volver", callback_data="mp")])

        return keyboard
    
    
    def menu_mensajes(self, usuario):
        n_msg = usuario.mensajes_sin_votar()
        if n_msg:
            n_msg = " - 🆕%s🆕" % n_msg
        else:
            n_msg = ""

        keyboard = [[InlineKeyboardButton("📨 Añadir mensajes", callback_data="ms_new")],
                    [InlineKeyboardButton("🔍 Votar mensajes%s" % n_msg, callback_data="ms_rev")],
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

        keyboard = [[InlineKeyboardButton("👎️", callback_data="revisar_valor_1down-%s" % msgID),
                     InlineKeyboardButton("⏭", callback_data="revisar_valor_skip-%s" % msgID),
                     InlineKeyboardButton("👍", callback_data="revisar_valor_1up-%s" % msgID),
                     InlineKeyboardButton("👍👍️", callback_data="revisar_valor_2up-%s" % msgID)],

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

    
    def menu_add_picante(self, mensaje):  # todo: actualizar las llamadas
        pic_dicc = {0: "❄️",
                    Constantes.PartidaClasica.VALOR_PICANTE_BAJO: "♨️",
                    Constantes.PartidaClasica.VALOR_PICANTE_MEDIO: "🌶",
                    Constantes.PartidaClasica.VALOR_PICANTE_ALTO: "🔥"}
        repe_dicc = {False: "¿Mensaje repetible? ❎ No",
                     True: "¿Mensaje repetible? ✅ Si"}

        keyboard = [[InlineKeyboardButton("⬅️❄️", callback_data="pic_menos_picante"),
                     InlineKeyboardButton("%s" % pic_dicc[mensaje.picante], callback_data="nanainanull"),
                     InlineKeyboardButton("🔥➡️", callback_data="pic_mas_picante")],

                    [InlineKeyboardButton(repe_dicc[mensaje.repetible], callback_data="pic_switch_repetible")],

                    [InlineKeyboardButton("❌ Cancelar", callback_data="ms_new"),
                     InlineKeyboardButton("Hecho 👌", callback_data="pic_done")]]
        return keyboard

    # EN PARTIDA    
    
    def menu_ecuesta_emparejador(self, descartes_restantes):

        if descartes_restantes:
            keyboard = [[InlineKeyboardButton("❌ - Ni de coña, nada", callback_data="emp-0")],
                         [InlineKeyboardButton("1️⃣ - Mejor no, pero bueno", callback_data="emp-1")],
                         [InlineKeyboardButton("2️⃣ - No me importaría", callback_data="emp-2")],
                         [InlineKeyboardButton("3️⃣ - Sería divertido", callback_data="emp-3")],
                         [InlineKeyboardButton("4️⃣ - No estaría nada mal", callback_data="emp-4")],
                         [InlineKeyboardButton("5️⃣ - Por favor, que ocurra ya", callback_data="emp-5")]]
        else:
            keyboard = [[InlineKeyboardButton("1️⃣ - Mejor no, pero bueno", callback_data="emp-1")],
                         [InlineKeyboardButton("2️⃣ - No me importaría", callback_data="emp-2")],
                         [InlineKeyboardButton("3️⃣ - Sería devertido", callback_data="emp-3")],
                         [InlineKeyboardButton("4️⃣ - No estaría nada mal", callback_data="emp-4")],
                         [InlineKeyboardButton("5️⃣ - Por favor, que ocurra ya", callback_data="emp-5")]]

        return keyboard

    @staticmethod
    def menu_mensaje():

        keyboard = [[InlineKeyboardButton("⚙️ / 🚪", callback_data="pc_ajustes"),
                     InlineKeyboardButton("🛑👎", callback_data="pc_vote_down"),
                     InlineKeyboardButton("👍💚", callback_data="pc_vote_up"),
                     InlineKeyboardButton("✉️⏭", callback_data="pc_next")]]
        return keyboard

    @staticmethod
    def menu_votar_partida():
        #todo: DEPRECATED
        keyboard = [[InlineKeyboardButton("👎", callback_data="pc_vote_down"),
                     InlineKeyboardButton("✉️⏭", callback_data="pc_next"),
                     InlineKeyboardButton("👍", callback_data="pc_vote_up")]]
        return keyboard

    @staticmethod
    def menu_ajustes_partida_clasica(emparejador=False):

        keyboard = []
        if not emparejador:
            keyboard.append([InlineKeyboardButton("❌👤Eliminar jugador", callback_data="apc_delete_player"),
                             InlineKeyboardButton("Añadir jugador➕👤", callback_data="apc_add_player")])

        keyboard.append([InlineKeyboardButton("❄️⬅️Menos picante", callback_data="apc_menos_picante"),
                         InlineKeyboardButton("Más picante➡️🔥", callback_data="apc_mas_picante")])

        keyboard.append([InlineKeyboardButton("🚪🏃‍♀️Salir", callback_data="apc_salir"),
                         InlineKeyboardButton("Volver⏭", callback_data="apc_volver")])
        return keyboard

    @staticmethod
    def menu_eliminar_jugador(jugadores):
        """La lista de jugadores se supone una lista de objetos jugador"""

        keyboard = [[InlineKeyboardButton("✅ Hecho", callback_data="delete_player_done")]]

        for jugador in jugadores:

            keyboard.append([InlineKeyboardButton(text=jugador.nombre, callback_data="delete_player*%s" % jugador.nombre)])

        return keyboard


Teclados = Teclados()


class Menus():
    """Todos los menús que necesita Piloco"""

    
    def menu_principal(self, usuario):

        msg = "🏠*MENÚ PRINCIPAL\n\n¡Bienvenido a Piloco!*\n\n¿listas para emborracharse?\nUsa los botones para navegar por los menús."

        keyboard = Teclados.menu_principal(usuario)
        return msg,keyboard

    
    def menu_partidaClasica(self, picante, emparejador, last_players):

        msg = "▶️*PARTIDA CLÁSICA*\n\nConfigura tu partida y pulsa iniciar partida."

        keyboard = Teclados.menu_partidaClasica(picante, emparejador, last_players)
        return msg, keyboard

    
    def menu_mensajes(self, usuario):

        msg = "✉️*MENSAJES*\n\nDesde aquí puedes añadir, votar o corregir mensajes que más tarde aparecerán en el j" \
              "uego."

        keyboard = Teclados.menu_mensajes(usuario)
        return msg, keyboard

    
    def menu_info(self, usuario):

        msg = "ℹ️*INFORMACIÓN*\n\n▪️[Canal oficial de Piloco](t.me/Piloco), *noticias y otros.*\n▪️¿Tienes *ideas nuevas" \
              "* para Piloco, o *alguna duda*? [Habla con nosotros](t.me/PilocoSupportbot)\n▪️Tienes *%s puntos de " \
              "reputación* [¿qué es eso?](telegra.ph/reputación-y-recompensas-05-27)\n\n" \
              "v1.0-alpha34" % int(usuario.reputacion)
        keyboard = Teclados.menu_info()
        return msg, keyboard

    @staticmethod
    def menu_eliminar_jugador(jugadores):

        msg = "Okay, pulsa abajo los botones con los nombres de los jugadores que quieres eliminar, " \
              "después, pulsa hecho."
        keyboard = Teclados.menu_eliminar_jugador(jugadores)
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
            jugadores += u"%s{0}" %nombre

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

    
    def menu_add_picante(self, mensaje):

        if mensaje.tipo == "normal":
            text0 = mensaje.text
            text1 = None
        elif mensaje.text1:
            text0 = mensaje.text0
            text1 = mensaje.text1
        else:
            text0 = mensaje.text
            text1 = None

        if text1:
            msg = u"Tu mensaje:\n\n\"%s\"\n\"%s\"\n\nNivel de picante: " % (text0, text1)
        else:
            msg = u"Tu mensaje:\n\n\"%s\"\n\nNivel de picante: " % (text0)

        if mensaje.picante >= Constantes.PartidaClasica.VALOR_PICANTE_ALTO:
            msg += u"*muy picante* 🔥"
        elif mensaje.picante >= Constantes.PartidaClasica.VALOR_PICANTE_MEDIO:
            msg += u"*picante* 🌶"
        elif mensaje.picante > 0:
            msg += u"*ligeramente picante* ♨️"
        else:
            msg += u"*nada picante* ❄️"

        keyboard = Teclados.menu_add_picante(mensaje)
        return msg, keyboard


Menus = Menus()
