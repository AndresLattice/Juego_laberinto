"""Reglas de la partida: turnos, movimiento, aparición y persecución."""

from dado import Dado
from fantasma_ia import buscar_camino_con_traza

META = (14, 14)
DISTANCIA_MIN_FANTASMA = 6
DIRECCIONES = {
    "arriba": (0, -1),
    "derecha": (1, 0),
    "abajo": (0, 1),
    "izquierda": (-1, 0),
}


class Partida:
    def __init__(self, laberinto, azar):
        self.azar = azar
        self.dado_jugador = Dado(azar)
        self.dado_fantasma = Dado(azar)
        self.reiniciar(laberinto)

    def reiniciar(self, laberinto):
        self.laberinto = laberinto
        self.jugador = (0, 0)
        self.fantasma = None
        self.turno = 1
        self.pasos = 0
        self.estado = "JUGADOR_TIRAR"
        self.traza = None
        self.camino = []
        self.aparecio = False

    def tirar(self):
        if self.estado != "JUGADOR_TIRAR":
            return
        self.pasos = self.dado_jugador.tirar()
        self.estado = "JUGADOR_MOVER"

    def mover(self, direccion):
        if self.estado != "JUGADOR_MOVER" or self.pasos == 0:
            return
        dc, df = DIRECCIONES[direccion]
        destino = (self.jugador[0] + dc, self.jugador[1] + df)
        if destino not in self.laberinto.vecinos_accesibles(self.jugador):
            return

        self.jugador = destino
        self.pasos -= 1
        if destino == META:
            self.estado = "VICTORIA"
        elif destino == self.fantasma:
            self.estado = "DERROTA"
        elif self.pasos == 0:
            self.terminar_turno()

    def terminar_turno(self):
        if self.estado != "JUGADOR_MOVER":
            return
        self.aparecio = False
        if self.fantasma is None:
            self.aparecer_fantasma()
            self.aparecio = True
        self.estado = "FANTASMA_TIRAR"

    def aparecer_fantasma(self):
        opciones = []
        distancias = self.laberinto.distancias_desde(self.jugador)
        for casilla in distancias:
            if distancias[casilla] >= DISTANCIA_MIN_FANTASMA and casilla != META:
                opciones.append(casilla)
        # Ordenar para que la misma semilla elija siempre la misma casilla.
        opciones.sort()
        self.fantasma = self.azar.choice(opciones)

    def tirar_fantasma(self):
        if self.estado != "FANTASMA_TIRAR":
            return None
        valor = self.dado_fantasma.tirar()
        camino, traza = buscar_camino_con_traza(self.laberinto, self.fantasma, self.jugador)
        self.traza = traza
        self.camino = camino[:valor]
        self.estado = "FANTASMA_MOVER"
        return traza

    def paso_fantasma(self):
        if self.estado != "FANTASMA_MOVER":
            return
        self.fantasma = self.camino.pop(0)
        if self.fantasma == self.jugador:
            self.estado = "DERROTA"
        elif len(self.camino) == 0:
            self.turno += 1
            self.estado = "JUGADOR_TIRAR"
