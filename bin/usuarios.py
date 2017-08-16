# coding=utf-8

import time, json
from .constantes import Constantes
import mensaje

class AjustesUsuario:

    def __init__(self, picante, emparejador):

        self.picante = picante
        self.emparejador = emparejador

    def actualizar(self, **kargs):

        self.picante = kargs.get("picante", self.picante)
        self.emparejador = kargs.get("emparejador", self.emparejador)


class Usuario:

    def __init__(self, idTelegram, **kargs):

        self.id = int(idTelegram)
        self.ultimo_uso = kargs.get("ultimo_uso", time.time())
        self.editando_mensaje = None
        self.partida = None
        self.ultimos_jugadores = kargs.get("ultimos_jugadores", [])
        self.reputacion = kargs.get("reputacion", Constantes.Usuarios.REPUTACION_INICIAL)
        self.ajustes = AjustesUsuario(picante=kargs.get("picante", 0), emparejador=kargs.get("emparejador", False))
        self.json_dump = json.dump  # sin esto no se puden guardar los usuarios, ya que json se cierra antes.

    def mensajes_sin_votar(self):

        n_msgs = 0
        id = self.id

        for mensaj in mensaje.MensajesEnRevision.list:
            if id not in mensaj.a_favor and id not in mensaj.skipped and id  not in mensaj.en_contra:
                n_msgs += 1
        return n_msgs


    def add_player(self, name):

        self.ultimos_jugadores.append(name.lower())

    def actualizar(self):
        self.ultimo_uso = time.time()

    def __del__(self):

        with open("users/%s.piuser" % self.id, "w") as f:

            dicc = {"ultimo_uso": self.ultimo_uso,
                    "ultimos_jugadores": self.ultimos_jugadores,
                    "reputacion": self.reputacion,
                    "picante": self.ajustes.picante,
                    "emparejador": self.ajustes.emparejador}

            self.json_dump(dicc, f, indent=2)


class Usuarios:

    def __init__(self):

        self.activos = []

    def _get_inx(self, idTelegram):

        """Devuelve el índice en el que debería colocarse el usuario para mantener ordenada la lista"""

        inx = 0
        for e in self.activos:
            if e.id > idTelegram:
                return inx
            inx += 1
        return inx

    def _bin_search(self, idTelegram):  # TODO: hay cosas mal aquí

        try:
            if idTelegram == self.activos[len(self.activos) - 1].id:
                return len(self.activos) - 1
        except: pass

        if len(self.activos):
            min = 0
            max = len(self.activos) - 1
            if max < 0:
                max = 0
            pic = max/2

            if idTelegram == self.activos[pic].id:
                return pic

            while pic != min and pic != max:

                if idTelegram < self.activos[pic].id:
                    max = pic
                    pic = (pic - min)/2 + min
                elif idTelegram > self.activos[pic].id:
                    min = pic
                    pic = (max - pic)/2 + pic

                if idTelegram == self.activos[pic].id:
                    return pic

        return None

    def _add_user(self, idTelegram, **kargs):
        """Carga el usuario de id proporcionana en la lista de activos.
        Si no se especifica archivo con file creará un nuevo usuario."""

        user = kargs.get("file", 0)

        if user:
            self.activos.insert(self._get_inx(idTelegram),
                                Usuario(idTelegram,
                                        ultimo_uso=user["ultimo_uso"],
                                        ultimos_jugadores=user["ultimos_jugadores"],
                                        reputacion=user["reputacion"],
                                        picante=user["picante"],
                                        emparejador=user["emparejador"]))
        else:
            self.activos.insert(self._get_inx(idTelegram),
                                Usuario(idTelegram,
                                        reputacion=kargs.get("reputacion", Constantes.Usuarios.REPUTACION_INICIAL)))

        return self._bin_search(idTelegram)

    def get_user(self, idTelegram):

        search = self._bin_search(idTelegram)
        if search != None:
            usuario = self.activos[search]
            usuario.actualizar()
            return usuario

        try:
            with open("users/%s.piuser" % idTelegram) as f:
                search = self._add_user(idTelegram, file=json.load(f))
            usuario = self.activos[search]

            cambio_reputacion = int((time.time() - usuario.ultimo_uso) / 86400)

            if usuario.reputacion - cambio_reputacion > 100:
                usuario.reputacion -= cambio_reputacion
            elif usuario.reputacion > 100:
                usuario.reputacion = 100

            usuario.actualizar()
            return usuario
        except:
            search = self._add_user(idTelegram)
            usuario = self.activos[search]

            with open("users/usuarios") as f:
                la_lista = json.load(f)

            la_lista.append(usuario.id)
            la_lista = list(set(la_lista))
            la_lista.sort()

            with open("users/usuarios", "w") as f:
                json.dump(la_lista, f)

            return usuario

    def actualizar_reputacion(self, idTelegram, reputacion):

        usuario = self.get_user(idTelegram)

        usuario.reputacion += reputacion

    def imprimir_estado(self):

        for usuario in self.activos:

            msg = "Usuario %s," % usuario.id

            if usuario.partida:

                msg += " con partida creada y"

            if usuario.editando_mensaje:

                msg += " editando mensaje y"

            msg += " activo hace %d segundos" % (time.time() - usuario.ultimo_uso)

            print msg

Usuarios = Usuarios()
