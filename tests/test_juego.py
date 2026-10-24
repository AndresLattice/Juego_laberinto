"""Aceptación de las reglas de la partida (spec 005)."""

import random

import pytest


class AzarFijo:
    """Doble que entrega los valores del dado en el orden indicado."""

    def __init__(self, valores):
        self.valores = list(valores)

    def randint(self, a, b):
        return self.valores.pop(0)

    def choice(self, opciones):
        return opciones[0]


@pytest.fixture
def tablero(registros):
    from laberinto import Laberinto
    return Laberinto(registros[0]["grid"])


def casilla_a_distancia(tablero, origen, pasos):
    for casilla, distancia in tablero.distancias_desde(origen).items():
        if distancia == pasos:
            return casilla


DIRECCIONES = {"arriba": (0, -1), "derecha": (1, 0), "abajo": (0, 1), "izquierda": (-1, 0)}


def mover_hacia(partida, destino):
    """Mover al jugador una casilla vecina usando la dirección correcta."""
    columna, fila = partida.jugador
    for nombre, (dc, df) in DIRECCIONES.items():
        if (columna + dc, fila + df) == destino:
            partida.mover(nombre)
            return


def test_inicio_de_partida(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([]))
    assert partida.jugador == (0, 0)
    assert partida.fantasma is None
    assert partida.turno == 1
    assert partida.estado == "JUGADOR_TIRAR"


def test_tirar_da_pasos_y_permite_mover(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([4]))
    partida.tirar()
    assert partida.pasos == 4
    assert partida.estado == "JUGADOR_MOVER"


def test_no_se_tira_dos_veces(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([4]))
    partida.tirar()
    partida.tirar()
    assert partida.pasos == 4


def test_pared_no_mueve_ni_gasta(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([3]))
    partida.tirar()
    for nombre, (dc, df) in DIRECCIONES.items():
        destino = (dc, df)
        if destino not in tablero.vecinos_accesibles((0, 0)):
            partida.mover(nombre)
            assert partida.jugador == (0, 0)
            assert partida.pasos == 3


def test_paso_valido_descuenta(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([3]))
    partida.tirar()
    vecino = tablero.vecinos_accesibles((0, 0))[0]
    mover_hacia(partida, vecino)
    assert partida.jugador == vecino
    assert partida.pasos == 2


def test_sin_pasos_no_se_mueve(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([3]))
    partida.mover("derecha")
    assert partida.jugador == (0, 0)
    partida.tirar()
    partida.pasos = 0
    mover_hacia(partida, tablero.vecinos_accesibles((0, 0))[0])
    assert partida.jugador == (0, 0)


def test_enter_antes_de_tirar_no_hace_nada(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([]))
    partida.terminar_turno()
    assert partida.estado == "JUGADOR_TIRAR"


def test_enter_tras_dos_de_cinco_pasa_al_fantasma(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([5]))
    partida.tirar()
    vecino = tablero.vecinos_accesibles((0, 0))[0]
    mover_hacia(partida, vecino)
    mover_hacia(partida, (0, 0))
    assert partida.pasos == 3
    partida.terminar_turno()
    assert partida.estado == "FANTASMA_TIRAR"


def test_fantasma_aparece_al_terminar_el_primer_turno(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([1]))
    partida.tirar()
    assert partida.fantasma is None
    partida.terminar_turno()
    assert partida.fantasma is not None
    assert partida.aparecio


def test_pasos_en_cero_terminan_el_turno(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([1]))
    partida.tirar()
    mover_hacia(partida, tablero.vecinos_accesibles((0, 0))[0])
    assert partida.estado == "FANTASMA_TIRAR"


def test_diez_mil_apariciones(tablero):
    from juego import Partida
    azar = random.Random(3)
    partida = Partida(tablero, azar)
    for i in range(10000):
        partida.jugador = (azar.randint(0, 14), azar.randint(0, 14))
        partida.aparecer_fantasma()
        distancias = tablero.distancias_desde(partida.jugador)
        assert distancias[partida.fantasma] >= 6
        assert partida.fantasma != (14, 14)


def preparar_fantasma(tablero, distancia, dado):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([dado]))
    partida.jugador = (7, 7)
    partida.fantasma = casilla_a_distancia(tablero, (7, 7), distancia)
    partida.estado = "FANTASMA_TIRAR"
    return partida


def test_captura_en_el_tercer_paso(tablero):
    partida = preparar_fantasma(tablero, 3, 5)
    traza = partida.tirar_fantasma()
    assert traza[-1].tipo == "encontrado"
    assert partida.estado == "FANTASMA_MOVER"
    partida.paso_fantasma()
    partida.paso_fantasma()
    assert partida.estado == "FANTASMA_MOVER"
    partida.paso_fantasma()
    assert partida.estado == "DERROTA"
    assert partida.fantasma == (7, 7)


def test_avanza_cuatro_sin_captura(tablero):
    partida = preparar_fantasma(tablero, 8, 4)
    partida.tirar_fantasma()
    for i in range(4):
        partida.paso_fantasma()
    distancias = tablero.distancias_desde((7, 7))
    assert distancias[partida.fantasma] == 4
    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.turno == 2


def test_victoria_con_pasos_de_sobra(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([6]))
    partida.tirar()
    vecino = tablero.vecinos_accesibles((14, 14))[0]
    partida.jugador = vecino
    mover_hacia(partida, (14, 14))
    assert partida.estado == "VICTORIA"
    partida.mover("arriba")
    assert partida.jugador == (14, 14)


def test_jugador_entra_al_fantasma(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([6]))
    partida.tirar()
    vecino = tablero.vecinos_accesibles((0, 0))[0]
    partida.fantasma = vecino
    mover_hacia(partida, vecino)
    assert partida.estado == "DERROTA"
    assert partida.pasos == 5


def test_reiniciar(tablero, registros):
    from laberinto import Laberinto
    partida = preparar_fantasma(tablero, 3, 5)
    partida.tirar_fantasma()
    nuevo = Laberinto(registros[1]["grid"])
    partida.reiniciar(nuevo)
    assert partida.laberinto is nuevo
    assert partida.jugador == (0, 0)
    assert partida.fantasma is None
    assert partida.traza is None
    assert partida.turno == 1
    assert partida.estado == "JUGADOR_TIRAR"


def test_acciones_fuera_de_estado(tablero):
    from juego import Partida
    partida = Partida(tablero, AzarFijo([]))
    partida.tirar_fantasma()
    partida.paso_fantasma()
    assert partida.estado == "JUGADOR_TIRAR"
