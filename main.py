# coding=utf-8
print "Importando librerias..."
import json, logging

#offlineMode = False           #sin implementar

from cosas import Partida, TOKEN, Usuario, error, enviarMensaje, debbugPrint, CB_newMessage_normal, CB_noDisponible, CB_newMessage_picante, CB_newMessage_hef, CB_newMessage_done
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
#podría dar error por eliminar import telegram.

print "Librerias importadas"

print "Declarando bot..."
updater = Updater(token=TOKEN)
del TOKEN
dispatcher = updater.dispatcher
print "Bot updater y dispatcher declarados"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

print "Declarando objetos y variables..."
Partidas = Partida()
Usuarios = Usuario()
with open("newMessages ") as f:
    newMessages = json.load(f) # en esta variable meteremos los mensajes que quieran aportar los usuarios.
print "Objetos y variables declarados"

print "Borrando usuarios demasiado antiguos..."
Usuarios.borrarUsuarios()
print "Usuarios borrados"

print "Leyendo lista de mensajes..."
with open("pilocuras.json") as f:
    mensajesPrincipal = json.load(f)
del f
print "Mensajes leidos"

"""---COMANDOS---"""

print "Declarando handlers..."
def comandoNew(bot,update):
    try:
       print "Ejectutando new para el usuario ", update.message.from_user.first_name
       idUsuario = update.message.from_user.id
       sesiones = Usuarios.usuariosActivos #para comprobar la posición del usuario
       posicionUsuarioEnSesiones = Usuarios.finder(idUsuario)
       if posicionUsuarioEnSesiones == None or sesiones[posicionUsuarioEnSesiones]["posicion"] == 0:
           print "Ejecutando new/if"
           Usuarios.actualizarUsuario(idUsuario,1)
           Partidas.nuevaPartida(idUsuario,[],mensajesPrincipal,Usuarios.usuariosActivos[Usuarios.finder(idUsuario)]["ajustes"])
           bot.send_message(chat_id=update.message.chat_id,text="Bien, ahora mandame los nombres de los jugadores uno por uno.")
       else:
           print "Ejecutando new/else"
           bot.send_message(chat_id=update.message.chat_id,text="¡Antes debes cancelar la partida!\nUsa /cancel.")
    except Exception,e:
        error(e,bot,update)
nuevoHandler = CommandHandler("new", comandoNew)
dispatcher.add_handler(nuevoHandler)

def comandoCancel(bot,update):
    try:
       print "Ejectutando cancel para el usuario ", update.message.from_user.first_name
       idUsuario = update.message.from_user.id
       Usuarios.actualizarUsuario(idUsuario,0)
       posicionPartida = Partidas.finder(idUsuario)
       posicionSesion = Usuarios.finder(idUsuario)

       if posicionPartida == None:
           pass
       else:
            Partidas.partidasEnCurso.pop(posicionPartida)
       bot.send_message(chat_id=update.message.chat_id, text="Cancelado.")

       """Para evitar errores con los usuarios que están añadiendo mensajes:"""
       #todo: el código de abajo daría problemas, hay que encontrar otra solución
       # if Usuarios.usuariosActivos[posicionSesion]["editando"] != None:
       #     newMessages.pop(Usuarios.usuariosActivos[posicionSesion]["editando"])
       #     Usuarios.usuariosActivos[posicionSesion]["editando"] = None

    except Exception,e:
        error(e, bot, update)
nuevoHandler = CommandHandler("cancel", comandoCancel)
dispatcher.add_handler(nuevoHandler)

def comandoDone(bot,update):
    try:
     idUsuario = update.message.from_user.id
     sesiones = Usuarios.usuariosActivos  # para comprobar la posición del usuario
     posicionUsuarioEnSesiones = Usuarios.finder(idUsuario)
     posicionPartida = Partidas.finder(idUsuario)
     if sesiones[posicionUsuarioEnSesiones]["posicion"] == 1 and len(Partidas.partidasEnCurso[posicionPartida]["jugadores"])>1:
         bot.send_message(chat_id=update.message.chat_id,
                          text="Iniciando la partida.\nPara pasar a la siguiente ronda escribe /next")
         enviarMensaje(bot,update,Partidas,Usuarios)
         Usuarios.actualizarUsuario(idUsuario, 2)
     else:
         print "Ejecutando done/else"
         bot.send_message(chat_id=update.message.chat_id, text="Necesito que me des más de un jugador para empezar la partida.")
    except Exception,e:
        error(e, bot, update)
nuevoHandler = CommandHandler("done", comandoDone)
dispatcher.add_handler(nuevoHandler)

def comandoNext(bot,update):
    try:
        print "Ejectutando next para el usuario ", update.message.from_user.first_name


        idUsuario = update.message.from_user.id
        sesiones = Usuarios.usuariosActivos  # para comprobar la posición del usuario
        posicionUsuarioEnSesiones = Usuarios.finder(idUsuario)
        if sesiones[posicionUsuarioEnSesiones]["posicion"] == 2:
            enviarMensaje(bot, update, Partidas, Usuarios)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="No tienes ninguna partida en curso.")
    except Exception,e:
        error(e, bot, update)
nuevoHandler = CommandHandler("next", comandoNext)
dispatcher.add_handler(nuevoHandler)

def comandoStart(bot, update):
    try:
        print "Ejectutando start para el usuario ",update.message.from_user.first_name
        mensaje = "¡Hola!\nPara empezar una nueva partida escribe /new"
        bot.send_message(chat_id=update.message.chat_id, text=mensaje)
        Usuarios.actualizarUsuario(update.message.from_user.id,0)
    except Exception,e:
        error(e, bot, update)
nuevoHandler = CommandHandler("start", comandoStart)
dispatcher.add_handler(nuevoHandler)

def comandoAjustes(bot,update):
    try:
        print "Ejecutando settings para, ",update.message.from_user.first_name
        usuarioAjustes = Usuarios.usuariosActivos[Usuarios.finder(update.message.from_user.id)]["ajustes"]
        mensaje = "Tus ajustes actuales son:\n"
        if usuarioAjustes["hastaElFondo"] == True:
            mensaje = mensaje + "Mensajes \"Hasta el fondo\" *ACTIVADOS*. Usa /hef para desactivarlos\n"
        else:
            mensaje = mensaje + "Mensajes \"hasta el fondo\" *DESACTIVADOS*. Usa /hef para activarlos\n"
        if usuarioAjustes["picante"] == True:
            mensaje = mensaje + "Mensajes \"piacantes\" *ACTIVADOS*. Usa /pi para desactivarlos\n"
        else:
            mensaje = mensaje + "Mensajes \"picantes\" *DESACTIVADOS*. Usa /pi para activarlos\n"
        mensaje = mensaje + "*" + str(usuarioAjustes["rondas"]) + "* rondas por partida. \"/rondas (aquí Nº de rondas)\" para ajustarlo"
        bot.send_message(chat_id=update.message.from_user.id,text=mensaje,parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception,e:
        error(e, bot, update)
nuevoHandler = CommandHandler("settings", comandoAjustes)
dispatcher.add_handler(nuevoHandler)

def comandoPi(bot,update):
    try:
        print "Ejecutando pi para ",update.message.from_user.first_name
        idUsuario = update.message.from_user.id
        usuarioAjustes = Usuarios.usuariosActivos[Usuarios.finder(idUsuario)]["ajustes"]
        if usuarioAjustes["picante"] == True:
            Usuarios.usuariosActivos[Usuarios.finder(idUsuario)]["ajustes"]["picante"] = False
            bot.send_message(chat_id=idUsuario,text="Se han desactivado los mensajes picantes para la próxima partida.")
        else:
            Usuarios.usuariosActivos[Usuarios.finder(idUsuario)]["ajustes"]["picante"] = True
            bot.send_message(chat_id=idUsuario, text="Podrian parecer mensajes picantes en la siguiente partida.")
    except Exception,e:
        error(e,bot,update)
nuevoHandler  = CommandHandler("pi", comandoPi)
dispatcher.add_handler(nuevoHandler)

def comandoHef(bot,update):
    try:
        print "Ejecutando hef para ",update.message.from_user.first_name
        idUsuario = update.message.from_user.id
        usuarioAjustes = Usuarios.usuariosActivos[Usuarios.finder(idUsuario)]["ajustes"]
        if usuarioAjustes["hastaElFondo"] == True:
            Usuarios.usuariosActivos[Usuarios.finder(idUsuario)]["ajustes"]["hastaElFondo"] = False
            bot.send_message(chat_id=idUsuario,text="Se han desactivado los mensajes \"hasta el fondo\" para la próxima"
                                                    " partida.")
        else:
            Usuarios.usuariosActivos[Usuarios.finder(idUsuario)]["ajustes"]["hastaElFondo"] = True
            bot.send_message(chat_id=idUsuario, text="Podrian parecer mensajes \"hasta el fondo\" en la siguiente parti"
                                                     "da.")
    except Exception,e:
        error(e, bot, update)
nuevoHandler  = CommandHandler("hef", comandoHef)
dispatcher.add_handler(nuevoHandler)

def comandoRondas(bot,update):
    print "Ejecutando rondas para ",update.message.from_user.first_name
    try:
        rondas = update.message.text
        rondas = int(rondas.replace("/rondas ",""))
        posUsu = Usuarios.finder(update.message.from_user.id)
        Usuarios.usuariosActivos[posUsu]["ajustes"]["rondas"] = rondas
        msg = "Tu siguiente partida durara {0} rondas."
        msg = msg.format(rondas)
        bot.send_message(chat_id=update.message.from_user.id,text=msg)
    except Exception,e:
        print e
        bot.send_message(chat_id=update.message.from_user.id,text="Tienes que enviarme un número así:\n/rondas #")
nuevoHandler = CommandHandler("rondas",comandoRondas)
dispatcher.add_handler(nuevoHandler)

def comandoRestart(bot,update):
    print "Ejectuando restart para el usuario ",update.message.from_user.first_name
    try:
        idUsuario = update.message.from_user.id
        bot.send_message(chat_id=idUsuario,text="Reiniciando tu usuario en el bot. Se cerrará tu partida actual y se re"
                                                "estableceran tus ajustes.")
        posicionPartida = Partidas.finder(idUsuario)
        posicionUsuario = Usuarios.finder(idUsuario)
        if posicionPartida != None:
            Partidas.partidasEnCurso.pop(posicionPartida)
        if posicionUsuario != None:
            Usuarios.usuariosActivos.pop(posicionUsuario)
        comandoStart(bot,update)
    except Exception, e:
        error(e, bot, update)
nuevoHandler = CommandHandler("restart", comandoRestart)
dispatcher.add_handler(nuevoHandler)

def comandoAbout(bot,update):
    msg = "Actualmente este bot está funcionando en la versión *BETA 1.4*\n[Más info](github.com/vetu11/piloco)"
    bot.send_message(chat_id=update.message.from_user.id,text=msg,parse_mode=ParseMode.MARKDOWN,disable_web_page_preview=True)
nuevoHandler = CommandHandler("about",comandoAbout)
dispatcher.add_handler(nuevoHandler)

def comandoHelp(bot,update):
    bot.send_message(chat_id=update.message.from_user.id,text="_Todavía no hay nada que ver aquí..._",parse_mode=telegram.ParseMode.MARKDOWN)
nuevoHandler =  CommandHandler("help",comandoHelp)
dispatcher.add_handler(nuevoHandler)

def comandoDelPlayer(bot,update):
    try:
        mensajeRec = update.message.text
        partida = Partidas.partidasEnCurso[Partidas.finder(update.message.from_user.id)]
        if mensajeRec == "/delplayer":
            mensaje = "Estos son los jugadores:\n"
            indice = 0
            while indice < len(partida["jugadores"]):
                mensaje = mensaje +     str(indice)+ ": " + partida["jugadores"][indice] + "\n"
                indice = indice + 1
            mensaje = str(mensaje) + "Ahora escribe /delplayer (Nº de jugador) para eliminarlo de la partida."
            bot.send_message(chat_id=update.message.from_user.id,text=mensaje)
        else:
            try:
                indice = int(mensajeRec.replace("/delplayer ", ""))
                jugador = partida["jugadores"][indice]
                Partidas.partidasEnCurso[Partidas.finder(update.message.from_user.id)]["jugadores"].pop(indice)
                msg = "El jugador {0} ha sido eliminado de la partida."
                msg = msg.format(jugador)
                bot.send_message(chat_id=update.message.from_user.id, text=msg)
            except:
                bot.send_message(chat_id=update.message.from_user.id,text="Tienes que enviarme un número así:\n/delplayer"
                                                                          " #")
    except Exception,e:
        error(e,bot,update)
nuevoHandler = CommandHandler("delplayer",comandoDelPlayer)
dispatcher.add_handler(nuevoHandler)

def comandoNewMessage(bot,update):
    try:
        #TODO: primero hay que comprobar si los usuarios están o no en una partida, sino se puede liar parda.

        msg = "Bien, ahora elige el tipo de mensaje que quieres hacer.\n*RECUERDA:*\n-normal: simple, de un sólo mens" \
              "aje.\n-RI: dos mensajes seguidos.\n-RNI: dos mensajes probablemente alejados."

        keyboard = [[InlineKeyboardButton("normal", callback_data="newMessage_normal"),
                     InlineKeyboardButton("RI", callback_data="newMessage_RI"),
                     InlineKeyboardButton("RNI", callback_data="newMessage_RNI")],

                    [InlineKeyboardButton("AYUDA POFABÓ 🆘", url="telegra.ph/Okay-03-12")]]

        update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
    except Exception,e:
        error(e,bot,update)
nuevoHandler = CommandHandler("newMessage", comandoNewMessage)
dispatcher.add_handler(nuevoHandler)


def mensaje(bot,update):
    try:
       print "Ejectutando mensaje para el usuario ", update.message.from_user.first_name
       idUsuario = update.message.from_user.id
       sesiones = Usuarios.usuariosActivos  # para comprobar la posición del usuario
       posicionUsuarioEnSesiones = Usuarios.finder(idUsuario)

       if posicionUsuarioEnSesiones == None:
           bot.send_message(chat_id=idUsuario,text="Parece que tienes que usar /start.\nEstamos trabajando en soluciona"
                                                   "r esto.")

       elif sesiones[posicionUsuarioEnSesiones]["posicion"] == 1: # AÑADIENDO JUGADORES A LA LISTA
           Partidas.partidasEnCurso[Partidas.finder(idUsuario)]["jugadores"].append(update.message.text)
           if len(Partidas.partidasEnCurso[Partidas.finder(idUsuario)]["jugadores"]) <2:
               mensaje = "Por favor, si quieres cancelar usa /cancel"
           else:
               mensaje = "Cuando hayas terminado escribe /done\nPor favor, si quieres cancelar usa /cancel"
           bot.send_message(chat_id=update.message.chat_id,text=mensaje)


       elif sesiones[posicionUsuarioEnSesiones]["posicion"] == 4: # AÑADIENDO MENSAJES NUEVOS A LA LISTA

            pos = len(newMessages)

            newMessages.append({"id":None})
            newMessages[pos]["tipo"] = "normal"
            newMessages[pos]["variantes"] = []
            newMessages[pos]["text"] = update.message.text

            print "%s ha añadido un nuevo mensaje."%(update.message.from_user.id)

            Usuarios.usuariosActivos[posicionUsuarioEnSesiones]["editando"] = pos

            s = update.message.text
            msg = 'Tu mensaje\n"%s"\nSelecciona categorías.' % s.encode('utf-8')

            keyboard = [[InlineKeyboardButton("Picante ❎", callback_data="newMessage_picante"),
                         InlineKeyboardButton("Hasta el fondo ❎", callback_data="newMessage_hef")],

                        [InlineKeyboardButton("Hecho 👌", callback_data="newMessage_done")]]

            update.message.reply_text(msg,reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)

       else:
           bot.send_message(chat_id=update.message.chat_id,text="No entiendo que quieres decir.")

    except Exception,e:
        error(e, bot, update)

nuevoHandler = MessageHandler([Filters.text], mensaje)
dispatcher.add_handler(nuevoHandler)


def inlineKeyboardCallback(bot, update):
    try:

        data = update.callback_query.data

        if data == "newMessage_normal":
            CB_newMessage_normal(bot,update,Usuarios)
        elif data == "newMessage_RI":
            CB_noDisponible(bot, update, Usuarios)
            #TODO
        elif data == "newMessage_RI":
            CB_noDisponible(bot, update, Usuarios)
            #TODO
        elif data == "newMessage_picante":
            CB_newMessage_picante(bot, update, Usuarios, newMessages)
        elif data == "newMessage_hef":
            CB_newMessage_hef(bot, update, Usuarios, newMessages)
        elif data == "newMessage_done":
            CB_newMessage_done(bot, update, Usuarios)

    except Exception,e:
        error(e,bot,update) #todo: test no envía el mensaje: update ya no sirve cuando es query
nuevoHandler = CallbackQueryHandler(inlineKeyboardCallback)
dispatcher.add_handler(nuevoHandler)

del nuevoHandler

#TODO: añadir un error handler
print "Handlers declarados"

print "Iniciando bot..."
updater.start_polling()
print "Bot iniciado"


while True:
    input_C = raw_input(">")

    if input_C == "stop":
        print "Guardando usuarios..."
        Usuarios.guardarUsuarios()
        print "Usuarios guardados"

        print "Guardando nuevos mensajes..."
        i = 0
        for e in newMessages:
            if "variantes" in e:
                if len(e["variantes"]) == 0:
                    newMessages[i].pop("variantes")
            i = i + 1

        with open("newMessages","w") as f:
            json.dump(newMessages,f,indent=4)
        print "Nuevos mensajes guardados"

        print "Apagando bot..."
        updater.stop()
        print "Bot apagado"
        break