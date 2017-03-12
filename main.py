# coding=utf-8
print "Importando librerias..."
import json, logging

#offlineMode = False           #sin implementar

from cosas import Partida, TOKEN, Usuario, error, enviarMensaje
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, inlinequeryhandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
#podrían producirse errores por la elimincación de import telegram.

print "Librerias importadas"

print "Declarando bot..."
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
print "Bot updater y dispatcher declarados"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

print "Declarando objetos y variables..."
Partidas = Partida()
Usuarios = Usuario()
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
       Partidas.partidasEnCurso.pop(posicionPartida)
       bot.send_message(chat_id=update.message.chat_id, text="Cancelado.")
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
    bot.send_message(chat_id=update.message.from_user.id,text="Actualmente este bot está funcionando en la versión BET"
                                                              "A 1.3\nNovedades:\n-Se han añadido mensajes\n-Se ha aña"
                                                              "dido el comando /delplayer\n-Se ha añadido la opción par"
                                                              "a editar el número de rondas por partida (/rondas)\n-Lig"
                                                              "eras optimizaciónes de rendimiento.")
    bot.send_message(chat_id=update.message.from_user.id,text="Si crees que este bot no se comporta como debería o si "
                                                              "tienes alguna sugerencia escribe a @vetu11. Gracias por"
                                                              " usar este bot.")
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
        msg = "Bien, ahora elige el tipo de mensaje que quieres hacer."

        keyboard = [[InlineKeyboardButton("normal", callback_data="normal"),
                     InlineKeyboardButton("RI", callback_data="RI"),
                     InlineKeyboardButton("RNI", callback_data="RNI")],

                    [InlineKeyboardButton("AYUDA POFABÓ", callback_data="help")]]

        update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        #bot.send_message(chat_id=update.message.from_user.id,text="Ahora mandame el nuevo mensaje que quieras añadir y "
        #                                                          "se revisará más tarde.\n*IMPORTANTE:* debes cumplir "
        #                                                          "ciertas normas para que el bot lo pueda enviar, usa "
        #                                                          "/rules para verlas.",parse_mode=telegram.ParseMode.MARKDOWN)
        #TODO: Resolver respuestas posibiles.
    except Exception,e:
        error(e,bot,update)
nuevoHandler = CommandHandler("newMessage", comandoNewMessage)
dispatcher.add_handler(nuevoHandler)

def comandoRules(bot,update):
    #TODO: el bot debería poner al usuario en un estado Neutro.
    try:
        id = update.message.from_user.id
        msg = "*Las reglas son las siguientes:*\n-Tu mensaje no puede contener comillas sueltas. Si quieres escribi" \
              "r comillas tendrás que poner *\\\"*\n-Para que el bot introduzca un nombre aleatorio debes escribir *" \
              "{1}* para un primer nombre y *{2}* para un segundo si quieres.\n"
        bot.send_message(chat_id=id,text=msg,parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception,e:
        error(e,bot,update)
nuevoHandler = CommandHandler("rules", comandoRules)
dispatcher.add_handler(nuevoHandler)

def mensaje(bot,update):
    try:
       print "Ejectutando mensaje para el usuario ", update.message.from_user.first_name
       idUsuario = update.message.from_user.id
       sesiones = Usuarios.usuariosActivos  # para comprobar la posición del usuario
       posicionUsuarioEnSesiones = Usuarios.finder(idUsuario)
       if posicionUsuarioEnSesiones == None:
           print "ejecutando mensaje/if"
           bot.send_message(chat_id=idUsuario,text="Parece que tienes que usar /start.\nEstamos trabajando en soluciona"
                                                   "r esto.")
       elif sesiones[posicionUsuarioEnSesiones]["posicion"] == 1:
           print "Ejecutando mensaje/añadir jugador"
           Partidas.partidasEnCurso[Partidas.finder(idUsuario)]["jugadores"].append(update.message.text)
           if len(Partidas.partidasEnCurso[Partidas.finder(idUsuario)]["jugadores"]) <2:
               print "Ejecutando mensaje/añadir jugador/un jugador"
               mensaje = "Por favor, si quieres cancelar usa /cancel"
           else:
               print "Ejecutando mensaje/añadir jugador/mas de un jugador"
               mensaje = "Cuando hayas terminado escribe /done\nPor favor, si quieres cancelar usa /cancel"
           bot.send_message(chat_id=update.message.chat_id,text=mensaje)
           print Partidas.partidasEnCurso[Partidas.finder(idUsuario)]["jugadores"]
       else:
           print "ejecutando mensaje/else"
           bot.send_message(chat_id=update.message.chat_id,text="No entiendo que quieres decir.")
    except Exception,e:
        error(e, bot, update)
nuevoHandler = MessageHandler([Filters.text], mensaje)
dispatcher.add_handler(nuevoHandler)
del nuevoHandler
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

        print "Apagando bot..."
        updater.stop()
        print "Bot apagado"
        break