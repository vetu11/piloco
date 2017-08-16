# coding=utf-8

import random
from .emparejador import Nodo, UnionDeNodos, Eleccion, Relacion
from .constantes import Constantes
from .mensaje import MensajesClasica, MensajeEnJuego


class ColaEmparejador:

    PEDIR_MOVIL = 0
    ENCUESTA = 1
    TERMINAR_ENCUESTAS = 2

    def __init__(self, accion, nodo1=None, nodo2=None):

        self.accion = accion
        self.nodo1 = nodo1
        self.nodo2 = nodo2


class Jugador(Nodo):

    def __init__(self, nombre, emparejador=False, partida=None):

        self.nombre = nombre

        if emparejador: Nodo.__init__(self, nombre, partida)


class BasePartidaClasica:

    todo_mensaje = MensajesClasica

    def __init__(self, padre, factor_picante, **kargs):  # TODO: eliminar padre, (está para backwards compatibilty)

        self.jugadores = []
        self.factor_picante = factor_picante
        self.valor_picante = kargs.get("valor_picante", Constantes.PartidaClasica.VALOR_INICIAL_PICANTE)
        self.mensajes = [[], []]
        self.last_message = None
        self.emparejador = None

        jugadores = kargs.get("jugadores", [])
        for nombre_jugador in jugadores:
            self.jugadores.append(Jugador(nombre_jugador.capitalize(), emparejador=padre.ajustes.emparejador, partida=self))

    def inciar_mensajes(self):

        while len(self.mensajes[0]) < Constantes.PartidaClasica.MENSAJES_INICIALES:
            self.mensajes[0].append(self.todo_mensaje.escojer_mensaje())

    def recargar_mensaje(self, mensaje=None):

        if not mensaje:
            for n in range((15 - len(self.mensajes[1]))):
                while 1:
                    msg = self.todo_mensaje.escojer_mensaje()
                    if msg not in self.mensajes[0] and msg not in self.mensajes[1]:
                        self.mensajes[1].append(msg)
                        break
        else:
            self.mensajes[1].append(mensaje)

    def introducir_nombres(self, mensaje, nombre1, nombre2):

        if mensaje.tipo == "RI":

            # INTRODUCIMOS LOS NOMBRES EN LOS TEXTOS
            text0 = mensaje.text0.replace("nombre1", nombre1) \
                .replace("nombre2", nombre2) \
                .format("", nombre1, nombre2)
            text1 = mensaje.text1.replace("nombre1", nombre1) \
                .replace("nombre2", nombre2) \
                .format("", nombre1, nombre2)

            msg_dicc = {"tipo": "normal",
                        "text": text1,
                        "puntuacion": mensaje.puntuacion,
                        "picante": mensaje.picante,
                        "id": mensaje.id,
                        "hecho_por": mensaje.hecho_por}

            self.mensajes[0].append(MensajeEnJuego(msg_dicc))
            self.mensajes[0][-1].original_id = mensaje.id  # 30-06 esto... No la lia, verdad?

        elif mensaje.tipo == "RNI":

            text0 = mensaje.text0.replace("nombre1", nombre1) \
                .replace("nombre2", nombre2) \
                .format("", nombre1, nombre2)
            text1 = mensaje.text1.replace("nombre1", nombre1) \
                .replace("nombre2", nombre2) \
                .format("", nombre1, nombre2)

            msg_dicc = {"tipo": "normal",
                        "text": text1,
                        "puntuacion": mensaje.puntuacion,
                        "picante": mensaje.picante,
                        "id": mensaje.id,
                        "hecho_por": mensaje.hecho_por}

            self.mensajes[1].append(MensajeEnJuego(msg_dicc))
            self.mensajes[1][-1].original_id = mensaje.id

        else:
            text0 = mensaje.text.replace("nombre1", nombre1) \
                .replace("nombre2", nombre2) \
                .format("", nombre1, nombre2)

        return text0


class PartidaClasica(BasePartidaClasica):

    def __init__(self, padre, factor_picante, **kwargs):

        BasePartidaClasica.__init__(self, padre, factor_picante, **kwargs)
        self.emparejador = False

    def elegir_jugadores(self):

        jugador1 = self.jugadores[random.randint(0, len(self.jugadores) -1)]
        jugador2 = self.jugadores[random.randint(0, len(self.jugadores) -1)]

        while jugador1 == jugador2:
            jugador2 = self.jugadores[random.randint(0, len(self.jugadores) -1)]

        return jugador1, jugador2

    def dame_mensaje(self):
        while 1:

            if not len(self.mensajes[0]):
                self.mensajes.reverse()
                self.mensajes[0].reverse()

            mensaje = self.mensajes[0].pop(-1)
            self.recargar_mensaje()

            try:
                mensaje.original_id
                picante_aceptado = True
            except:
                picante_aceptado = False
                if self.valor_picante >= mensaje.picante:
                    diferencia_picante = self.valor_picante - mensaje.picante
                    pic = random.randint(-12, round(diferencia_picante))
                    if pic <= 0 or self.mensajes[1] <= 5: picante_aceptado = True

            if picante_aceptado:

                jugador1, jugador2 = self.elegir_jugadores()
                nombre1, nombre2 = jugador1.nombre.capitalize(), jugador2.nombre.capitalize()

                text0 = self.introducir_nombres(mensaje, nombre1, nombre2)
                break

        self.last_message = mensaje
        if self.factor_picante:
            self.valor_picante += self.factor_picante
        return text0

    def add_player(self, name):
        """Añade un objeto jugador con el nombre indicado"""

        self.jugadores.append(Jugador(name.lower(), self.emparejador, self))

    def iniciar_valor_picante(self):

        self.valor_picante *= self.factor_picante

        if self.factor_picante == Constantes.PartidaClasica.FACTOR_PICANTE_BAJO:
            self.factor_picante = Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO
        elif self.factor_picante == Constantes.PartidaClasica.FACTOR_PICANTE_MEDIO:
            self.factor_picante = Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO
        elif self.factor_picante == Constantes.PartidaClasica.FACTOR_PICANTE_ALTO:
            self.factor_picante = Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO

    def mas_picante(self):

        dic_fac_picante = [0,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO]  # TODO: preguntar a ruso si esto es mejor como atributo de la clase

        actual = dic_fac_picante.index(self.factor_picante)

        if actual < len(dic_fac_picante) - 1:
            nuevo = actual + 1
            self.valor_picante *= 2
        else:
            nuevo = actual

        self.factor_picante = dic_fac_picante[nuevo]

    def menos_picante(self):

        dic_fac_picante = [0,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO]

        actual = dic_fac_picante.index(self.factor_picante)

        if actual > 0:
            nuevo = actual - 1
        else:
            nuevo = actual

        self.factor_picante = dic_fac_picante[nuevo]
        self.valor_picante /= 2


class PartidaClasicaEmparejador(BasePartidaClasica, UnionDeNodos):

    def __init__(self, padre, factor_picante, **kargs):

        BasePartidaClasica.__init__(self, padre, factor_picante, **kargs)
        UnionDeNodos.__init__(self)
        self.emparejador = True
        self.acciones_pendientes = []

    def relaciones_aptas(self, valor_picante):

        relaciones = []

        for relacion in self.relaciones:

            if relacion.potencia >= valor_picante:

                relaciones.append(relacion)
        return relaciones

    def dame_mensaje(self):
        while 1:

            if not len(self.mensajes[0]):
                self.mensajes.reverse()
                self.mensajes[0].reverse()

            mensaje = self.mensajes[0].pop(-1)
            self.recargar_mensaje()

            relaciones_aptas = self.relaciones_aptas(mensaje.picante)
            picante_aceptado = False
            if relaciones_aptas:
                relacion = relaciones_aptas[random.randint(0, len(relaciones_aptas) - 1)]

                try:
                    mensaje.original_id
                    picante_aceptado = True
                except:
                    if relacion.potencia >= mensaje.picante:
                        diferencia_picante = relacion.potencia - mensaje.picante
                        pic = random.randint(-12, round(diferencia_picante))
                        if pic <= 0 or self.mensajes[1] <= 5: picante_aceptado = True


            if picante_aceptado:
                if random.randint(0,1):
                    nombre1, nombre2 = relacion.n1.nombre.capitalize(), relacion.n2.nombre.capitalize()
                else:
                    nombre2, nombre1 = relacion.n1.nombre.capitalize(), relacion.n2.nombre.capitalize()

                text0 = self.introducir_nombres(mensaje, nombre1, nombre2)
                break

        self.last_message = mensaje

        if self.factor_picante:
            for relacion in self.relaciones:
                if relacion.potencia:
                    relacion.potencia += self.factor_picante

        return text0

    def add_player(self, name):

        self.jugadores.append(Jugador(nombre=name,
                                      emparejador=True,
                                      partida=self))

    def iniciar_valor_picante(self):

        for relacion in self.relaciones:
            relacion.potencia *= self.factor_picante

        if self.factor_picante == Constantes.PartidaClasica.FACTOR_PICANTE_BAJO:
            self.factor_picante = Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO
        elif self.factor_picante == Constantes.PartidaClasica.FACTOR_PICANTE_MEDIO:
            self.factor_picante = Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO
        else:
            self.factor_picante = Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO

    def iniciar_cola(self):

        for nodo1 in self.jugadores:

            self.acciones_pendientes.append(ColaEmparejador(ColaEmparejador.PEDIR_MOVIL,
                                                            nodo1=nodo1))

            for nodo2 in self.jugadores:

                if nodo1 != nodo2:

                    self.acciones_pendientes.append(ColaEmparejador(ColaEmparejador.ENCUESTA,
                                                                    nodo1=nodo1,
                                                                    nodo2=nodo2))

        self.acciones_pendientes.append(ColaEmparejador(ColaEmparejador.TERMINAR_ENCUESTAS))
        self.acciones_pendientes.reverse()

    def mas_picante(self):

        dic_fac_picante = [0,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO]

        actual = dic_fac_picante.index(self.factor_picante)

        if actual < len(dic_fac_picante) - 1:
            nuevo = actual + 1
            for relacion in self.relaciones:
                relacion.potencia *= 2
        else:
            nuevo = actual

        self.factor_picante = dic_fac_picante[nuevo]

    def menos_picante(self):

        dic_fac_picante = [0,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_BAJO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_MEDIO,
                           Constantes.PartidaClasica.FACTOR_RONDA_PICANTE_ALTO]

        actual = dic_fac_picante.index(self.factor_picante)

        if actual > 0:
            nuevo = actual - 1
        else:
            nuevo = actual

        self.factor_picante = dic_fac_picante[nuevo]

        for relacion in self.relaciones:
            relacion.potencia /= 2
