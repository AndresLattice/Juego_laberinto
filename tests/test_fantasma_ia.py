"""Aceptación de la búsqueda con traza del fantasma (spec 004)."""

import pytest


def laberintos(registros):
    from laberinto import Laberinto
    return [Laberinto(registro["grid"]) for registro in registros]


def test_origen_igual_destino(registros):
    from fantasma_ia import buscar_camino, buscar_camino_con_traza
    tablero = laberintos(registros)[0]
    assert buscar_camino(tablero, (3, 3), (3, 3)) == []
    camino, traza = buscar_camino_con_traza(tablero, (3, 3), (3, 3))
    assert camino == []
    assert [(e.tipo, e.casilla, e.pila) for e in traza] == [
        ("apilar", (3, 3), ((3, 3),)),
        ("encontrado", (3, 3), ((3, 3),)),
    ]


def test_camino_valido(registros):
    from fantasma_ia import buscar_camino
    for tablero in laberintos(registros):
        camino = buscar_camino(tablero, (0, 0), (14, 14))
        anterior = (0, 0)
        for casilla in camino:
            assert casilla in tablero.vecinos_accesibles(anterior)
            anterior = casilla
        assert camino[-1] == (14, 14)


def test_existe_camino_en_los_cinco(registros):
    from fantasma_ia import buscar_camino
    tableros = laberintos(registros)
    assert len(tableros) == 5
    for tablero in tableros:
        assert len(buscar_camino(tablero, (0, 0), (14, 14))) > 0


def test_inicio_y_fin_de_traza(registros):
    from fantasma_ia import buscar_camino_con_traza
    for tablero in laberintos(registros):
        camino, traza = buscar_camino_con_traza(tablero, (0, 0), (14, 14))
        assert (traza[0].tipo, traza[0].casilla) == ("apilar", (0, 0))
        assert (traza[-1].tipo, traza[-1].casilla) == ("encontrado", (14, 14))
        assert list(traza[-1].pila[1:]) == camino


def test_cuenta_de_apilar_y_desapilar(registros):
    from fantasma_ia import buscar_camino_con_traza
    for tablero in laberintos(registros):
        camino, traza = buscar_camino_con_traza(tablero, (0, 0), (14, 14))
        apilados = 0
        desapilados = 0
        for evento in traza:
            if evento.tipo == "apilar":
                apilados += 1
            elif evento.tipo == "desapilar":
                desapilados += 1
                assert apilados - desapilados >= 0
        assert apilados - desapilados == len(camino) + 1


def test_desapila_solo_la_cima_sin_salidas(registros):
    from fantasma_ia import buscar_camino_con_traza
    for tablero in laberintos(registros):
        camino, traza = buscar_camino_con_traza(tablero, (0, 0), (14, 14))
        visitados = set()
        pila_antes = ()
        retrocesos = 0
        for evento in traza:
            if evento.tipo == "apilar":
                visitados.add(evento.casilla)
            elif evento.tipo == "desapilar":
                retrocesos += 1
                assert pila_antes[-1] == evento.casilla
                for vecino in tablero.vecinos_accesibles(evento.casilla):
                    assert vecino in visitados
            pila_antes = evento.pila
        assert retrocesos > 0


def test_traza_determinista(registros):
    from fantasma_ia import buscar_camino_con_traza
    for tablero in laberintos(registros):
        primera = buscar_camino_con_traza(tablero, (0, 0), (14, 14))
        segunda = buscar_camino_con_traza(tablero, (0, 0), (14, 14))
        assert primera == segunda


class TableroPartido:
    """Doble mínimo: dos casillas unidas y el resto aislado."""

    def vecinos_accesibles(self, casilla):
        if casilla == (0, 0):
            return [(1, 0)]
        if casilla == (1, 0):
            return [(0, 0)]
        return []


def test_destino_inalcanzable():
    from fantasma_ia import buscar_camino, buscar_camino_con_traza
    with pytest.raises(ValueError):
        buscar_camino(TableroPartido(), (0, 0), (5, 5))
    with pytest.raises(ValueError):
        buscar_camino_con_traza(TableroPartido(), (0, 0), (5, 5))


def test_pila_maxima_en_tablero_serpiente(serpiente):
    from laberinto import Laberinto
    from fantasma_ia import buscar_camino_con_traza
    grid, posiciones = serpiente
    tablero = Laberinto(grid)
    camino, traza = buscar_camino_con_traza(tablero, posiciones[0], posiciones[-1])
    assert len(camino) == 224
    mayor = 0
    for evento in traza:
        if len(evento.pila) > mayor:
            mayor = len(evento.pila)
    assert mayor == 225


def test_distancias_coinciden_con_camino(registros):
    from fantasma_ia import buscar_camino
    for tablero in laberintos(registros):
        distancias = tablero.distancias_desde((0, 0))
        assert distancias[(0, 0)] == 0
        for casilla, pasos in distancias.items():
            assert pasos == len(buscar_camino(tablero, (0, 0), casilla))
