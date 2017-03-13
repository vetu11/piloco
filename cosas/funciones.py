#coding=utf-8
import random

def elegirNombre(listaDeNombres):
    nombre1 = listaDeNombres[random.randint(0, len(listaDeNombres) - 1)]
    nombre2 = listaDeNombres[random.randint(0, len(listaDeNombres) - 1)]
    if listaDeNombres > 1:
        while nombre2 is nombre1:
            print "elegirMensaje/elif/else/while"
            nombre2 = listaDeNombres[random.randint(0, len(listaDeNombres) - 1)]
    return nombre1,nombre2

def nuevosMensajes(listaDeMensajes,ajustesJugador):
    nMensajesEnLista = len(listaDeMensajes)
    nMensajesElegidos = ajustesJugador["rondas"]
    mensajeN = 0
    mensajesUsados = []
    mensajes = []
    print "Eligiendo mensajes. Se van a elegir ",nMensajesElegidos," de ",nMensajesEnLista," mensajes."
    antiLoop = 0
    while mensajeN < nMensajesElegidos:
        pic = random.randint(0,nMensajesEnLista-1)
        mensaje = listaDeMensajes[pic]
        if mensaje["id"] not in mensajesUsados:
            if "variantes" not in mensaje:
                mensajes.append(mensaje)
                mensajesUsados.append(mensaje["id"])
                mensajeN = mensajeN + 1
                antiLoop = 0
            elif "picante" in mensaje["variantes"] and "hastaElFondo" in mensaje["variantes"] and ajustesJugador["hastaElFondo"] == True and ajustesJugador["picante"] == True:
                mensajes.append(mensaje)
                mensajesUsados.append(mensaje["id"])
                mensajeN = mensajeN + 1
                antiLoop = 0
            elif "picante" in mensaje["variantes"] and ajustesJugador["picante"] == True:
                mensajes.append(mensaje)
                mensajesUsados.append(mensaje["id"])
                mensajeN = mensajeN + 1
                antiLoop = 0
            elif "hastaElFondo" in mensaje["variantes"] and ajustesJugador["hastaElFondo"] == True:
                mensajes.append(mensaje)
                mensajesUsados.append(mensaje["id"])
                mensajeN = mensajeN + 1
                antiLoop = 0
        if antiLoop > 50:
            print "Error de loop. Devolviendo menos mensajes de los pedidos."
            break
        antiLoop = antiLoop + 1
    return mensajes

def formatoMensaje(listaDeMensajes, listaDeNombres, bot, update, Partidas, Usuarios):
    nMensajes = len(listaDeMensajes)
    print "escogiendo mensajes ",nMensajes
    pic = random.randint(0,nMensajes - 1)
    print "pic = ",pic
    mensajeElegido = listaDeMensajes[pic]
    if mensajeElegido["tipo"] == "normal":
        nombre1,nombre2 = elegirNombre(listaDeNombres)
        mensaje = mensajeElegido["text"].format("",nombre1,nombre2)
        return mensaje,None,pic
    elif mensajeElegido["tipo"] == "RI":
        nombre1, nombre2 = elegirNombre(listaDeNombres)
        mensaje0 = mensajeElegido["text0"].format("", nombre1, nombre2)
        mensaje1 = mensajeElegido["text1"].format("", nombre1, nombre2)
        return mensaje0,mensaje1,pic
    elif mensajeElegido["tipo"] == "RNI":
        nombre1, nombre2 = elegirNombre(listaDeNombres)
        mensaje = mensajeElegido["text0"].format("", nombre1, nombre2)
        sigText = mensajeElegido["text1"].format("", nombre1, nombre2)
        sigMensaje = {"tipo":"normal","text":sigText}
        Partidas.partidasEnCurso[Partidas.finder(update.message.from_user.id)]["mensajes"].append(sigMensaje)
        return mensaje,None,pic

def enviarMensaje(bot,update,Partidas,Usuarios):
    print "Ejecutando enviarMensaje"
    idUsuario = update.message.from_user.id
    posicionPartida = Partidas.finder(idUsuario)
    listaDeMensajes = Partidas.partidasEnCurso[posicionPartida]["mensajes"]
    listaDeNombres = Partidas.partidasEnCurso[posicionPartida]["jugadores"]
    if len(listaDeMensajes) == 0 and Partidas.partidasEnCurso[posicionPartida]["siguiente"]["reap"] == False:
            print "Terminando partida"
            bot.send_message(chat_id=update.message.chat_id, text="······\nFin de la partida\nPara continuar empi"
                                                                  "eza una nueva con /new")
            Partidas.partidasEnCurso.pop(posicionPartida)
            Usuarios.actualizarUsuario(update.message.from_user.id, 0)
    else:
        if Partidas.partidasEnCurso[posicionPartida]["siguiente"]["reap"] == True:
            mensaje = Partidas.partidasEnCurso[posicionPartida]["siguiente"]["text"]
            Partidas.partidasEnCurso[posicionPartida]["siguiente"]["reap"] = False
        else:
            mensaje, x,pic = formatoMensaje(listaDeMensajes, listaDeNombres, bot, update, Partidas, Usuarios)
            Partidas.partidasEnCurso[posicionPartida]["mensajes"].pop(pic)
            if x != None:
                Partidas.partidasEnCurso[posicionPartida]["siguiente"]["reap"] = True
                Partidas.partidasEnCurso[posicionPartida]["siguiente"]["text"] = x
        bot.send_message(chat_id=update.message.chat_id, text=mensaje)

def error(e,bot,update):
    print "ERROR\n", e
    bot.send_message(chat_id=update.message.chat_id, text="Oh oh. Parece que ha ocurrido un error. Por favor, informa a"
                                                          " @vetu11.\nSi el error persiste usa /restart")

def debbugPrint(txt):
    print txt