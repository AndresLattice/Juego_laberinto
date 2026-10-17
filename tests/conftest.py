"""Datos de prueba independientes del módulo de lógica."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture
def registros():
    return json.loads((RAIZ / "base" / "laberintos.json").read_text(encoding="utf-8"))


@pytest.fixture
def grid(registros):
    return deepcopy(registros[0]["grid"])


@pytest.fixture
def cambiar():
    def cambiar_celda(tablero, fila, columna, caracter):
        copia = list(tablero)
        linea = copia[fila]
        copia[fila] = linea[:columna] + caracter + linea[columna + 1:]
        return copia
    return cambiar_celda


@pytest.fixture
def escribir_catalogo(tmp_path):
    def escribir(datos):
        ruta = tmp_path / "laberintos.json"
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return ruta
    return escribir


@pytest.fixture
def variantes_grafo(grid, cambiar):
    abiertas, cerradas = [], []
    grados = {(c, f): 0 for f in range(15) for c in range(15)}
    for f in range(15):
        for c in range(15):
            for dc, df in ((1, 0), (0, 1)):
                if c + dc >= 15 or f + df >= 15:
                    continue
                a, b = (c, f), (c + dc, f + df)
                posicion = (2 * f + 1 + df, 2 * c + 1 + dc)
                if grid[posicion[0]][posicion[1]] == " ":
                    abiertas.append((a, b, posicion))
                    grados[a] += 1
                    grados[b] += 1
                else:
                    cerradas.append((a, b, posicion))
    hoja = next(casilla for casilla, grado in grados.items() if grado == 1)
    corte = next(pos for a, b, pos in abiertas if hoja in (a, b))
    extra = next(pos for a, b, pos in cerradas if hoja not in (a, b))
    desconectado = cambiar(grid, *corte, "#")
    return {
        "ciclo": cambiar(grid, *extra, " "),
        "desconexion": desconectado,
        "desconexion_con224": cambiar(desconectado, *extra, " "),
    }


@pytest.fixture
def serpiente():
    posiciones = [(c, f) for f in range(15)
                  for c in (range(15) if f % 2 == 0 else range(14, -1, -1))]
    matriz = [["#"] * 31 for _ in range(31)]
    for c, f in posiciones:
        matriz[2 * f + 1][2 * c + 1] = " "
    for (c1, f1), (c2, f2) in zip(posiciones, posiciones[1:]):
        matriz[f1 + f2 + 1][c1 + c2 + 1] = " "
    matriz[1][0] = matriz[29][30] = " "
    return ["".join(fila) for fila in matriz], posiciones


@pytest.fixture
def distancias_referencia():
    def recorrer(g, origen):
        # Pila de posiciones del grid; no usa APIs ni utilidades de producción.
        c, f = origen
        pila = [(2 * f + 1, 2 * c + 1, 0)]
        resultado = {}
        while pila:
            fila, columna, pasos = pila.pop()
            casilla = ((columna - 1) // 2, (fila - 1) // 2)
            if casilla in resultado:
                continue
            resultado[casilla] = pasos
            for df, dc in ((2, 0), (-2, 0), (0, 2), (0, -2)):
                nf, nc = fila + df, columna + dc
                if 1 <= nf <= 29 and 1 <= nc <= 29:
                    if g[fila + df // 2][columna + dc // 2] == " ":
                        pila.append((nf, nc, pasos + 1))
        return resultado
    return recorrer
