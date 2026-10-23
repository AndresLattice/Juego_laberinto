"""Búsqueda del fantasma con backtracking y traza de la pila."""

from typing import NamedTuple


class Evento(NamedTuple):
    tipo: str
    casilla: tuple
    pila: tuple


def buscar_camino_con_traza(laberinto, origen, destino):
    """Devolver (camino, traza) desde origen hasta destino."""
    pila = [origen]
    visitados = {origen}
    traza = [Evento("apilar", origen, tuple(pila))]

    while len(pila) > 0:
        actual = pila[-1]
        if actual == destino:
            traza.append(Evento("encontrado", destino, tuple(pila)))
            return pila[1:], traza

        siguiente = None
        for vecino in laberinto.vecinos_accesibles(actual):
            if vecino not in visitados:
                siguiente = vecino
                break

        if siguiente is not None:
            pila.append(siguiente)
            visitados.add(siguiente)
            traza.append(Evento("apilar", siguiente, tuple(pila)))
        else:
            # Callejón sin salida: retroceder a la casilla anterior.
            pila.pop()
            traza.append(Evento("desapilar", actual, tuple(pila)))

    raise ValueError("No existe camino.")


def buscar_camino(laberinto, origen, destino):
    """Devolver solo el camino."""
    camino, traza = buscar_camino_con_traza(laberinto, origen, destino)
    return camino
