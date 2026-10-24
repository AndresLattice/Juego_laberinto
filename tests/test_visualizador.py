"""Aceptación del reproductor de la traza (spec 006)."""

import pytest


@pytest.fixture
def traza(registros):
    from laberinto import Laberinto
    from fantasma_ia import buscar_camino_con_traza
    tablero = Laberinto(registros[0]["grid"])
    camino, eventos = buscar_camino_con_traza(tablero, (0, 0), (14, 14))
    return eventos


def contar(eventos, tipo):
    total = 0
    for evento in eventos:
        if evento.tipo == tipo:
            total += 1
    return total


def test_espera_sin_traza():
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    assert reproductor.pila_visible == ()
    assert reproductor.esperando
    reproductor.actualizar(1)
    reproductor.paso()
    reproductor.saltar()
    assert reproductor.pila_visible == ()


def test_intervalo_de_la_spec(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    assert reproductor.intervalo == max(0.03, 4 / len(traza))
    assert not reproductor.esperando


def test_pila_visible_en_el_tiempo(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    reproductor.actualizar(reproductor.intervalo * 10.5)
    vistos = traza[:10]
    assert reproductor.evento_actual == vistos[-1]
    assert reproductor.pila_visible == vistos[-1].pila
    assert reproductor.apilados == contar(vistos, "apilar")
    assert reproductor.retrocesos == contar(vistos, "desapilar")
    assert reproductor.profundidad == len(vistos[-1].pila)


def test_marcas_del_tablero(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    reproductor.saltar()
    descartada = None
    for evento in traza:
        if evento.tipo == "desapilar":
            descartada = evento.casilla
    assert reproductor.estado_casilla(descartada) == "descartada"
    assert reproductor.estado_casilla(traza[-1].casilla) == "en_pila"
    assert reproductor.estado_casilla((99, 99)) is None


def test_saltar_llega_al_final(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    reproductor.saltar()
    assert reproductor.terminado
    assert reproductor.evento_actual == traza[-1]
    assert reproductor.pila_visible == traza[-1].pila
    assert reproductor.camino == list(traza[-1].pila[1:])
    assert reproductor.apilados == contar(traza, "apilar")
    assert reproductor.retrocesos == contar(traza, "desapilar")
    mayor = 0
    for evento in traza:
        if len(evento.pila) > mayor:
            mayor = len(evento.pila)
    assert reproductor.maximo == mayor


def test_pausa_y_paso(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    reproductor.paso()
    assert reproductor.evento_actual is None
    reproductor.pausar()
    reproductor.actualizar(100)
    assert reproductor.evento_actual is None
    reproductor.paso()
    assert reproductor.evento_actual == traza[0]
    assert reproductor.camino == []
    reproductor.paso()
    assert reproductor.evento_actual == traza[1]
    reproductor.pausar()
    reproductor.actualizar(reproductor.intervalo)
    assert reproductor.evento_actual == traza[2]


def test_pasos_al_terminar_no_hacen_nada(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    reproductor.saltar()
    reproductor.pausar()
    reproductor.paso()
    reproductor.actualizar(100)
    assert reproductor.evento_actual == traza[-1]


def test_velocidad_entre_limites(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    for i in range(5):
        reproductor.mas_rapido()
    assert reproductor.velocidad == 4
    for i in range(10):
        reproductor.mas_lento()
    assert reproductor.velocidad == 0.25
    reproductor.mas_rapido()
    reproductor.actualizar(reproductor.intervalo * 2)
    assert reproductor.evento_actual == traza[0]


def test_limpiar_borra_marcas(traza):
    from visualizador import ReproductorTraza
    reproductor = ReproductorTraza()
    reproductor.cargar(traza)
    reproductor.saltar()
    reproductor.limpiar()
    assert reproductor.esperando
    assert reproductor.pila_visible == ()
    assert reproductor.estado_casilla(traza[0].casilla) is None
    assert reproductor.apilados == 0


def test_traza_de_origen_igual_destino(registros):
    from laberinto import Laberinto
    from fantasma_ia import buscar_camino_con_traza
    from visualizador import ReproductorTraza
    tablero = Laberinto(registros[0]["grid"])
    camino, eventos = buscar_camino_con_traza(tablero, (3, 3), (3, 3))
    reproductor = ReproductorTraza()
    reproductor.cargar(eventos)
    assert reproductor.intervalo == 2
    reproductor.saltar()
    assert reproductor.camino == []
