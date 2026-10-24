"""Dado de seis caras con animación que no afecta la lógica."""

import random

DURACION = 0.6
CAMBIO = 0.06


class Dado:
    def __init__(self, azar_logico, azar_visual=None):
        self.azar_logico = azar_logico
        # Las caras que giran salen de otro generador para no cambiar la partida.
        if azar_visual is None:
            azar_visual = random.Random()
        self.azar_visual = azar_visual
        self.valor = None
        self.cara = None
        self.animando = False
        self.tiempo = 0
        self.cambios = 0

    def tirar(self):
        self.valor = self.azar_logico.randint(1, 6)
        self.cara = self.azar_visual.randint(1, 6)
        self.animando = True
        self.tiempo = 0
        self.cambios = 0
        return self.valor

    def actualizar(self, segundos):
        if not self.animando:
            return
        self.tiempo += segundos
        if self.tiempo >= DURACION:
            self.animando = False
            self.cara = self.valor
            return
        while self.cambios < int(self.tiempo / CAMBIO):
            self.cara = self.azar_visual.randint(1, 6)
            self.cambios += 1
