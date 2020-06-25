# coding=utf-8

import json, random, uuid
from .constantes import Constantes
from .usuarios import Usuarios

class Puntos:
    """VECTOR ORINTADO A LA PUNTUACIÓN DE UN MENSAJE"""

    def __init__(self, tupla):

        self.puntos = tupla

    def __iadd__(self, other):

        self.puntos = (round(self.puntos[0] + other.puntos[0], 1), round(self.puntos[1] + other.puntos[1], 1))

        return self

    def __call__(self, *args, **kwargs):

        return self.puntos

    def __mul__(self, other):

        return Puntos((self.puntos[0] * other, self.puntos[1] * other))


class BaseMensaje:

    def __init__(self, **kargs):

        self.tipo = kargs.get("tipo", "normal")
        self.picante = kargs.get("picante", 0)
        self.id = kargs.get("id", uuid.uuid4().get_hex()[:8])
        self.hecho_por = kargs.get("hecho_por")
        self.repetible = kargs.get("repetible", False)

        if self.tipo == "normal":
            self.text = kargs.get("text")
        else:
            self.text0 = kargs.get("text0")
            self.text1 = kargs.get("text1")


class MensajeEnRevision(BaseMensaje):

    def __init__(self, **kargs):

        BaseMensaje.__init__(self, **kargs)
        dicc_revisar = kargs.get("revisar", {"a_favor":[], "en_contra":[], "skipped":[], "puntos":(0, 0)})
        self.puntos = Puntos(dicc_revisar["puntos"])
        self.a_favor = dicc_revisar["a_favor"]
        self.en_contra = dicc_revisar["en_contra"]
        self.skipped = dicc_revisar["skipped"]


class MensajeEnJuego(BaseMensaje):

    def __init__(self, **kargs):

        BaseMensaje.__init__(self, **kargs)
        self.puntuacion = kargs.get("puntuacion")
        self.original_id = kargs.get("original_id")


class MensajesClasica:

    def __init__(self):

        self.list = []
        self.json_dump = json.dump

        with open("pilocuras.json") as f:
            list = json.load(f)

        for msg_dicc in list:

            self.list.append(MensajeEnJuego(**msg_dicc))

    def escojer_mensaje(self):

        return self.list[random.randint(0, len(self.list) - 1)]

    def get_new_id(self):

        if self.list:
            todasIDs = []
            idLibres = []

            for mensaje in self.list:
                todasIDs.append(mensaje.id)
            ultimaID = max(todasIDs)

            posicion = 0
            while posicion <= ultimaID:
                if posicion not in todasIDs:
                    idLibres.append(posicion)
                posicion = posicion + 1

            if idLibres:
                return idLibres[0]
            else:
                return ultimaID + 1
        else:
            return 0

    def transformar_a_en_revision(self, mensaje):  # 30-06:

        if mensaje.tipo == "normal":
            msg_dicc = {"id": uuid.uuid4().get_hex()[:8],
                        "tipo": mensaje.tipo,
                        "picante": mensaje.picante,
                        "text": mensaje.text,
                        "revision": {"puntos": (0, 0),
                                     "a_favor":[],
                                     "skipped":[],
                                     "en_contra":[]},
                        "hecho_por": mensaje.hecho_por}
        else:
            msg_dicc = {"id": uuid.uuid4().get_hex()[:8],
                        "tipo": mensaje.tipo,
                        "picante": mensaje.picante,
                        "text0": mensaje.text0,
                        "text1": mensaje.text1,
                        "revision": {"puntos": (0, 0),
                                     "a_favor":[],
                                     "skipped":[],
                                     "en_contra":[]},
                        "hecho_por": mensaje.hecho_por}

        return MensajeEnRevision(**msg_dicc)

    def comprobar_aptitud(self, mensaje):

        if mensaje.puntuacion <= -10:
            # sin este try/except, si se está el mensaje revisando cuando ya ha sido eliminado por otro
            # jugador, tendríamos problemas
            try:
                self.list.remove(mensaje)
                MensajesEnRevision.list.append(self.transformar_a_en_revision(mensaje))
            except:
                pass

    def get_message(self, msgID):

        for mensaje in self.list:
            if mensaje.id == int(msgID):
                return mensaje
        return None

    def guardar(self):
        print "Guardando mensajes..."
        list = []

        for mensaje in self.list:

            if mensaje.tipo == "normal":
                msg_dicc = {"hecho_por": mensaje.hecho_por,
                            "text": mensaje.text,
                            "tipo": mensaje.tipo,
                            "puntuacion": mensaje.puntuacion,
                            "repetible": mensaje.repetible,
                            "picante": mensaje.picante,
                            "id": mensaje.id}
            else:
                msg_dicc =   {"hecho_por": mensaje.hecho_por,
                              "text0": mensaje.text0,
                              "text1": mensaje.text1,
                              "tipo": mensaje.tipo,
                              "repetible": mensaje.repetible,
                              "puntuacion": mensaje.puntuacion,
                              "picante": mensaje.picante,
                              "id": mensaje.id}
            list.append(msg_dicc)

        with open("pilocuras.json", "w") as f:

            self.json_dump(list, f, indent=2)
        print "Mensajes guardados"

    def __del__(self):

        self.guardar()

MensajesClasica = MensajesClasica()


class MensajesEnRevision:

    def __init__(self):

        self.list = []
        self.json_dump = json.dump

        with open("newMessages.json") as f:
            list = json.load(f)

        for msg_dicc in list:

            self.list.append(MensajeEnRevision(**msg_dicc))

        self.renovar_revisiones(None, None, None, False)

    def renovar_revisiones(self, bot, update, args, from_telegram):

        if from_telegram:
            if update.message.from_user.id == 254234845:
                if args:
                    renovaciones = int(args[0])
                else:
                    renovaciones = 1

                for n in range(renovaciones):
                    a = self._actually_renew_revisions()
                    if not a:
                        break

                if a:
                    bot.send_message(254234845, "Se han completado %s renovaciones" % renovaciones)
                else:
                    bot.send_message(254234845, "No se ha llegado al limite de renovaciones")

        else:
            self._actually_renew_revisions()

    def escojer_mensaje(self, idTelegram=None):
        antiLoop = 0

        if not idTelegram:
            return self.list[random.randint(0, len(self.list) - 1)]
        else:
            while antiLoop < 100:

                mensaje = self.list[random.randint(0, len(self.list) - 1)]
                if idTelegram not in mensaje.a_favor and idTelegram not in mensaje.en_contra and idTelegram not in mensaje.skipped:
                    return mensaje
                antiLoop += 1
            return None

    def guardar(self):
        print "Guardan mensajes en revisión"
        list = []

        for mensaje in self.list:

            if mensaje.tipo == "normal":
                msg_dicc = {"hecho_por": mensaje.hecho_por,
                            "text": mensaje.text,
                            "tipo": mensaje.tipo,
                            "picante": mensaje.picante,
                            "repetible": mensaje.repetible,
                            "id": mensaje.id,
                            "revisar": {"a_favor": mensaje.a_favor,
                                        "en_contra": mensaje.en_contra,
                                        "skipped": mensaje.skipped,
                                        "puntos": mensaje.puntos()}}
            else:
                msg_dicc =   {"hecho_por": mensaje.hecho_por,
                              "text0": mensaje.text0,
                              "text1": mensaje.text1,
                              "tipo": mensaje.tipo,
                              "picante": mensaje.picante,
                              "repetible": mensaje.repetible,
                              "id": mensaje.id,
                              "revisar":{"a_favor": mensaje.a_favor,
                                         "en_contra": mensaje.en_contra,
                                         "skipped": mensaje.skipped,
                                         "puntos": mensaje.puntos()}}
            list.append(msg_dicc)

        with open("newMessages.json", "w") as f:

            self.json_dump(list, f, indent=2)
        print "Mensajes en revisión guardados"

    def __del__(self):

        self.guardar()

    def _actually_renew_revisions(self):
        if not self.list:
            return True
        mensaje = self.list[random.randint(0, len(self.list) - 1)]
        pic = random.randint(0, 2)
        if pic == 2 and mensaje.a_favor:
            mensaje.a_favor.pop(random.randint(0, len(mensaje.a_favor) - 1))
        elif pic == 1 and mensaje.skipped:
            mensaje.skipped.pop(random.randint(0, len(mensaje.skipped) - 1))
        elif not pic and mensaje.en_contra:
            mensaje.en_contra.pop(random.randint(0, len(mensaje.en_contra) - 1))
        return True

    def get_message(self, msgID):

        for mensaje in self.list:
            if mensaje.id == msgID:
                return mensaje
        return None

    def transformar_a_activo(self, mensaje):

        if mensaje.tipo == "normal":
            msg_dicc = {"id": MensajesClasica.get_new_id(),
                        "tipo": mensaje.tipo,
                        "picante": mensaje.picante,
                        "text": mensaje.text,
                        "puntuacion": 0,
                        "hecho_por": mensaje.hecho_por}
        else:
            msg_dicc = {"id": MensajesClasica.get_new_id(),
                        "tipo": mensaje.tipo,
                        "picante": mensaje.picante,
                        "text0": mensaje.text0,
                        "text1": mensaje.text1,
                        "puntuacion": 0,
                        "hecho_por": mensaje.hecho_por}

        return MensajeEnJuego(**msg_dicc)

    def comprobar_aptitud(self, mensaje):

        puntos_necesarios = Constantes.Usuarios.NUMERO_USUARIOS * 0.3

        puntos_tupla = mensaje.puntos.puntos

        if puntos_tupla[0] >= puntos_necesarios:
            self.list.remove(mensaje)
            MensajesClasica.list.append(self.transformar_a_activo(mensaje))

            Usuarios.actualizar_reputacion(mensaje.hecho_por, 20.0)
            for idTelegram in mensaje.a_favor:
                Usuarios.actualizar_reputacion(idTelegram, 1.0)
            for idTelegram in mensaje.en_contra:
                Usuarios.actualizar_reputacion(idTelegram, -1.0)

        elif puntos_tupla[0] <= -puntos_necesarios/3:
            self.list.remove(mensaje)

            Usuarios.actualizar_reputacion(mensaje.hecho_por, -5.0)
            for idTelegram in mensaje.a_favor:
                Usuarios.actualizar_reputacion(idTelegram, -1.0)
            for idTelegram in mensaje.en_contra:
                Usuarios.actualizar_reputacion(idTelegram, 1.0)

        elif puntos_tupla[1] <= -puntos_necesarios/3:
            pass
            # self.list.remove(mensaje)  # TODO: añadir a una lista de mensajes
            #
            # Usuarios.actualizar_reputacion(mensaje.hecho_por, -5.0)
            # for idTelegram in mensaje.a_favor:
            #     Usuarios.actualizar_reputacion(idTelegram, 1.0)
            # for idTelegram in mensaje.en_contra:
            #     Usuarios.actualizar_reputacion(idTelegram, -1.0)

MensajesEnRevision = MensajesEnRevision()
