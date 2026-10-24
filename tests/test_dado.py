"""Aceptación del dado y de la separación del azar (spec 003)."""

import random


class AzarContado:
    """Doble que cuenta cuántas veces se le pide un número."""

    def __init__(self):
        self.llamadas = 0

    def randint(self, a, b):
        self.llamadas += 1
        return 3


def test_diez_mil_tiradas():
    from dado import Dado
    dado = Dado(random.Random(1))
    vistas = set()
    for i in range(10000):
        valor = dado.tirar()
        assert 1 <= valor <= 6
        vistas.add(valor)
    assert vistas == {1, 2, 3, 4, 5, 6}


def test_cada_actor_guarda_su_tirada():
    from dado import Dado
    azar = random.Random(5)
    jugador = Dado(azar)
    fantasma = Dado(azar)
    valor_jugador = jugador.tirar()
    valor_fantasma = fantasma.tirar()
    assert jugador.valor == valor_jugador
    assert fantasma.valor == valor_fantasma


def test_misma_semilla_misma_secuencia():
    from dado import Dado
    primero = Dado(random.Random(123))
    segundo = Dado(random.Random(123))
    for i in range(50):
        assert primero.tirar() == segundo.tirar()


def test_animacion_cambia_cada_006_y_fija_el_valor():
    from dado import Dado
    visual = AzarContado()
    dado = Dado(random.Random(1), visual)
    valor = dado.tirar()
    assert dado.animando
    llamadas_iniciales = visual.llamadas
    dado.actualizar(0.059)
    assert visual.llamadas == llamadas_iniciales
    dado.actualizar(0.002)
    assert visual.llamadas == llamadas_iniciales + 1
    dado.actualizar(0.6)
    assert not dado.animando
    assert dado.cara == valor


def test_animacion_no_consume_azar_logico():
    from dado import Dado
    azar = random.Random(7)
    dado = Dado(azar)
    dado.tirar()
    estado = azar.getstate()
    for i in range(30):
        dado.actualizar(0.02)
    assert azar.getstate() == estado


def test_cuadros_distintos_misma_partida():
    from dado import Dado
    resultados = []
    for paso in (0.01, 0.1):
        dado = Dado(random.Random(99))
        valores = []
        for i in range(20):
            valores.append(dado.tirar())
            while dado.animando:
                dado.actualizar(paso)
        resultados.append(valores)
    assert resultados[0] == resultados[1]


def test_actualizar_sin_tirada_no_hace_nada():
    from dado import Dado
    visual = AzarContado()
    dado = Dado(random.Random(1), visual)
    dado.actualizar(1)
    assert visual.llamadas == 0
    assert dado.valor is None
