# coding=utf-8
import json, time, threading, random
from .funciones import nuevosMensajes

class Partida:
    partidasEnCurso = []

    def finder(self, host):
        print "finder de partida"
        posicionPartida = 0
        for e in self.partidasEnCurso:
            if e["host"] == host:
                return posicionPartida
            posicionPartida = posicionPartida + 1

    def nuevaPartida(self, host, jugadores,listaDeMensajes,ajustesJugador):
        print "creando partida"
        mensajes = nuevosMensajes(listaDeMensajes,ajustesJugador)
        self.partidasEnCurso.append({"host": host, "jugadores": jugadores,"mensajes": mensajes,"siguiente":{"reap":False,"text":None}})
        print "partida creada"

    def mensajeUsado(self, host, mensaje):
        print "marcando mensaje como usado"
        self.partidasEnCurso[self.finder(host)]["mensajesEnviados"].append(mensaje)

class Usuario:
    usuariosActivos = []

    def __init__(self):
        with open("usuarios") as f:
            self.usuariosActivos = json.load(f)

    def finder(self,idUsuario):
        print "Ejecutando finder de usuario para ", idUsuario
        posicionUsuarioEnLista = 0
        for e in self.usuariosActivos:
            if e["id"] == idUsuario:
                return posicionUsuarioEnLista
            posicionUsuarioEnLista = posicionUsuarioEnLista + 1
        return None

    def actualizarUsuario(self,idUsuario,posicion):
        posUsuLista = self.finder(idUsuario)
        if  posUsuLista != None:
            self.usuariosActivos[posUsuLista]["ultimoUso"] = time.time()
            self.usuariosActivos[posUsuLista]["posicion"] = posicion
        else:
            self.usuariosActivos.append({"id":idUsuario,"posicion":posicion,"ajustes":{"hastaElFondo":False,"picante":False,"rondas":30},"ultimoUso":time.time(),"editando":None})

    def guardarUsuarios(self):
        with open("usuarios","w") as f:
            json.dump(self.usuariosActivos,f,indent=4)

    def borrarUsuarios(self):
        pos = 0
        indice = 0
        for e in self.usuariosActivos:
            if e["ultimoUso"] < time.time() - 5184000:
                self.usuariosActivos.pop(pos)
            else:
                pos = pos + 1
            # hasta aquí borra los usuarios que no han usado el bot en los últimos 60 días

            # lo siguiente es para evitar que ocurra un error que ocurríria (aunque nunca ha ocurrido) cuando el servido
            #r se cierra mientras tiene usuarios activos, ya que al iniciar el bot estarían en posición y 2 sin partida.

            if e["posicion"] == 2:
                self.usuariosActivos[indice]["posicion"] = 0
            indice = indice + 1

    def actualizarMensaje(self, idUsuario, init=None, text=None):
        """Este método actuliza el mensaje que esté editando un usuario.
        init: establecerá un mensaje vacío del tipo que se especifique, normal/RI/RNI
        text: establecerá el texto del mensaje que esté editando el usuario
        variante: cambiará el valor una de las variantes del mensaje que es esté editando, picante/hef
        """

        posUsu = self.finder(idUsuario)


        if init != None:
            self.usuariosActivos[posUsu]["editando"] = {"id": hex(random.randint(0, 10 ** 8)).replace("0x", ""),
                                                        "variantes":[],
                                                        "revisar":{
                                                            "puntos":(0,0),
                                                            "revisado":[]}}

            if init == "normal":
                self.usuariosActivos[posUsu]["editando"]["tipo"] = "normal"
            elif init == "RI":
                self.usuariosActivos[posUsu]["editando"]["tipo"] = "RI"
            else:
                self.usuariosActivos[posUsu]["editando"]["tipo"] = "RNI"

        elif text != None:

            if self.usuariosActivos[posUsu]["editando"]["tipo"] == "normal":
                self.usuariosActivos[posUsu]["editando"]["text"] = unicode(text, encoding="utf-8")
            elif "text0" in self.usuariosActivos[posUsu]["editando"]:
                self.usuariosActivos[posUsu]["editando"]["text1"] = unicode(text, encoding="utf-8")
            else:
                self.usuariosActivos[posUsu]["editando"]["text0"] = unicode(text, encoding="utf-8")

"""
POSICIONES:
POSICION = 0: fuera de partida, después de acabarla o de escribir /start
POSICION = 1: esperando lista de jugadores por parte de este usuario
POSICION = 2: en partida
POSICION = 3: en ajustes/personalizar.
POSICION = 4: esperando nuevo mensaje de tipo normal
POSICION = 5: esperando nuevo mensaje de tipo RI (reaparición instantánea)
POSICION = 6: esperando nuevo mensaje de tipo RNI (reaparicón no instantánea)
POSOCION = 7: esperando segundo mensaje para RI o RNI.
"""