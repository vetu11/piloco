# coding=utf-8
import json,time,threading
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
            self.usuariosActivos.append({"id":idUsuario,"posicion":posicion,"ajustes":{"hastaElFondo":False,"picante":False,"rondas":30},"ultimoUso":time.time()})

    def guardarUsuarios(self):
        with open("usuarios","w") as f:
            json.dump(self.usuariosActivos,f,indent=True)

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


"""
POSICIONES:
POSICION = 0: fuera de partida, después de acabarla o de escribir /start
POSICION = 1: esperando lista de jugadores por parte de este usuario
POSICION = 2: en partida
POSICION = 3: en ajustes/personalizar.
POSICION = 4: esperando nuevo mensaje de tipo normal
POSICION = 5: esperando nuevo mensaje de tipo RI (reaparición instantánea)
POSICION = 6: esperando nuevo mensaje de tipo RNI (reaparicón no instantánea)
"""