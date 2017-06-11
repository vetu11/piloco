# coding=utf-8

from .constantes import Constantes


class Eleccion:

    def __init__(self, n1, n2, potencia):

        self.padre = n1
        self.apunta = n2
        self.potencia = potencia


class Relacion:

    def __init__(self, n1, n2):

        self.n1 = n1
        self.n2 = n2

        eleccionN1 = Nodo.buscar_eleccion(n1, n2)
        eleccionN2 = Nodo.buscar_eleccion(n2, n1)

        self.potencia = eleccionN1.potencia * eleccionN2.potencia

    def calcular_probabilidad(self):

        posibilidades = 0

        for relacion in self.n1.relaciones:

            posibilidades = posibilidades + relacion.potencia

        try:
            self.probabilidad = float(self.potencia) / float(posibilidades)
        except:
            self.probabilidad = self.potencia


class Nodo:

    def __init__(self, nombre, union):
        """Esta clase representa un nodo dentro del mapa de relaciones de la partida. Es un jugador."""

        self.id = nombre
        self.relaciones = [] # Objetos relacion
        self.relacionadoCon = [] # Nodos con los que se relaciona
        self.elecciones = [] # Objetos eleccion
        self.union = union
        self.descartes_restantes = Constantes.Emparejador.DESCARTES

    def elegir(self, n2, potencia):
        """Esta función crea una elección para para el nodo en cusetión que a punta a n2 con una potencia.
        Devuelve 1 si se ha añadido.
        Devuelve 0 si ya están relacionados."""

        if n2 not in self.relacionadoCon:
            self.elecciones.append(Eleccion(self, n2, potencia))
            return 1
        else:
            return 0

    def buscar_eleccion(self, n2):

        for eleccion in self.elecciones:

            if eleccion.apunta == n2:
                return eleccion

    def iniciar_relaciones(self):

        for otroNodo in self.union():

            if otroNodo.id != self.id and otroNodo not in self.relacionadoCon:

                self.relacionadoCon.append(otroNodo)
                otroNodo.relacionadoCon.append(self)

                self.relaciones.append(Relacion(self, otroNodo))
                otroNodo.relaciones.append(Relacion(otroNodo, self))

    def calcular_potencia(self):

        self.potenciaTotal = 0

        for relacion in self.relaciones:
            self.potenciaTotal += relacion.potencia

        return self.potenciaTotal

    def descarto(self):

        self.descartes_restantes -= 1


class UnionDeNodos:
    """Esta clase agrupa todos los nodos para relacionarlos todos juntos. No es relación 1Nodo-1Nodo."""

    def __init__(self):

        self.relaciones = []

    def _get_rel_index(self, relacion):
        index = 0

        for rel in self.relaciones:

            if rel.potencia > relacion.potencia:
                return index
            index += 1
        return index

    def inicializar_toda_relacion(self):

        for nodo in self.jugadores:

            nodo.iniciar_relaciones()

            for relacion in nodo.relaciones:

                if relacion not in self.relaciones:
                    self.relaciones.insert(self._get_rel_index(relacion), relacion)

    def __call__(self, *args, **kwargs):

        return self.jugadores
