# config=utf-8

import json

class PartidaClasica:

    VALOR_INICIAL_PICANTE = 12.5  # ES IMPORTANTE QUE SEA FLOAT PARA LAS DIVISIONES.
    FACTOR_PICANTE_NO_PICANTE = 0
    FACTOR_PICANTE_BAJO = 0.5
    FACTOR_PICANTE_MEDIO = 1
    FACTOR_PICANTE_ALTO = 2
    FACTOR_RONDA_PICANTE_BAJO = 1.001
    FACTOR_RONDA_PICANTE_MEDIO = 1.003
    FACTOR_RONDA_PICANTE_ALTO = 1.004
    VALOR_PICANTE_BAJO = 1.0
    VALOR_PICANTE_MEDIO = 9.0  # ES IMPORTANTE QUE SEA FLOAT PARA LAS DIVISIONES.
    VALOR_PICANTE_ALTO = 25.0  # ES IMPORTANTE QUE SEA FLOAT PARA LAS DIVISIONES.
    EMPAREJADOR_LIMITE_DESCARTES = 1
    MENSAJES_INICIALES = 10


class Usuarios:

    REPUTACION_INICIAL = 100.0  # ES IMPORTANTE QUE SEA FLOAT PARA LAS DIVISIONES.
    ACESO_A_ADD_MESSAGE = 50

    with open("users/usuarios") as f:
        NUMERO_USUARIOS = len(json.load(f))
    del f

class Emparejador:

    DESCARTES = 1


class Constantes:

    PartidaClasica = PartidaClasica
    Usuarios = Usuarios
    Emparejador = Emparejador
