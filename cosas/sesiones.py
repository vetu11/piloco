#coding=utf-8
class Sesion:
    sesiones = []
    usuarios = []

    def finder(self,idUsuario):
        posicionUsuariosEnSesiones = 0
        for e in self.usuarios:
            if e == idUsuario:
                return posicionUsuariosEnSesiones - 1
            posicionUsuariosEnSesiones = posicionUsuariosEnSesiones + 1
        return None

    def nuevaSesion(self,idUsuario,posicion):
        print "iniciando sesión... usuarios activos = ", self.usuarios, "sesiones: ",self.sesiones
        posicionUsuariosEnSesiones = self.finder(idUsuario)
        if idUsuario not in self.usuarios:
            print "ejecutando nuevaSesión/if"
            self.sesiones.append({"id":idUsuario,"posicion":posicion})
            self.usuarios.append(idUsuario)
        else:
            print "ejecutando nuevaSesión/else"
            self.sesiones[posicionUsuariosEnSesiones]["posicion"] = posicion

"""
POSICIONES:
POSICION = 0: fuera de partida, después de acabarla o de escribir /start
POSICION = 1: esperando lista de jugadores por parte de este usuario
POSICION = 2: en partida
POSICION = 3: en ajustes/personalizar.
"""