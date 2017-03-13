#coding=utf-8
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

def CB_newMessage_categorias_generarKEY(picante, hef):
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


def CB_newMessage_normal(bot,update,Usuarios):
    query = update.callback_query

    Usuarios.actualizarUsuario(update.callback_query.from_user.id,4)

    msg="Estas escribiendo un mensaje de tipo normal (de un sólo texto). Usa /cancel para cancelar.\n*RECUERDA:* Si q" \
        "uieres poner nombres de jugadores usa `{1}` para el primer nombre aleatorio y `{2}` para el segundo nombre."

    keyboard = [[InlineKeyboardButton("AYUDA 🆘", url="telegra.ph/Okay-03-12")]]

    bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=InlineKeyboardMarkup(keyboard),
                          parse_mode=ParseMode.MARKDOWN)


def CB_newMessage_picante(bot, update, Usuarios, newMessages):
    query = update.callback_query

    posUsu = Usuarios.finder(query.from_user.id)
    editando = Usuarios.usuariosActivos[posUsu]["editando"]

    variantesActuales = newMessages[editando]["variantes"]

    if "picante" not in variantesActuales:
        newMessages[editando]["variantes"].append("picante")
        picante = True
    else:
        newMessages[editando]["variantes"].remove("picante")
        picante = False

    if "hastaElFondo" in variantesActuales:
        hef = True
    else:
        hef = False

    keyboard = CB_newMessage_categorias_generarKEY(picante, hef)

    bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=InlineKeyboardMarkup(keyboard))

def CB_newMessage_hef(bot, update, Usuarios, newMessages):
    query = update.callback_query

    posUsu = Usuarios.finder(query.from_user.id)
    editando = Usuarios.usuariosActivos[posUsu]["editando"]

    variantesActuales = newMessages[editando]["variantes"]

    if "hastaElFondo" not in variantesActuales:
        newMessages[editando]["variantes"].append("hastaElFondo")
        hef = True
    else:
        newMessages[editando]["variantes"].remove("hastaElFondo")
        hef = False

    if "picante" in variantesActuales:
        picante = True
    else:
        picante = False

    keyboard = CB_newMessage_categorias_generarKEY(picante, hef)

    bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=InlineKeyboardMarkup(keyboard))

def CB_newMessage_done(bot, update, Usuarios):
    query = update.callback_query

    msg = "Gracias por tu aportación, el mensaje se incluirá próximamente."

    keyboard = [[]]

    bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=InlineKeyboardMarkup(keyboard))

    posUsu = Usuarios.finder(query.from_user.id)
    Usuarios.usuariosActivos[posUsu]["posicion"] = 0
    Usuarios.usuariosActivos[posUsu]["editando"] = None

def CB_noDisponible(bot,update,Usuarios):
    query = update.callback_query

    print "Se ha pedido una función no disponible."

    update.callback_query.message.reply_text("Esa función no está disponible todavía, cancelando.")

    posUsu = Usuarios.finder(update.callback_query.from_user.id)

    Usuarios.usuariosActivos[posUsu]["posicion"] = 0

    msg = "Work in progress. Vuelve a intentarlo en la próxima acutalización. Consulta la versión con /about"

    keyboard = [[]]

    bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=InlineKeyboardMarkup(keyboard))