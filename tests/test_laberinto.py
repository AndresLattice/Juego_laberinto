"""Aceptación de carga, movimiento y distancias sin interfaz gráfica."""

from copy import deepcopy
from dataclasses import FrozenInstanceError
import subprocess
import sys

import pytest


def test_normaliza_y_copia_grid(grid):
    from laberinto import Laberinto
    esperado = tuple(grid)
    tablero = Laberinto(grid)
    grid[1] = "#" * 31
    assert tablero.grid == esperado
    assert isinstance(tablero.grid, tuple)
    assert len(tablero.grid) == 31
    with pytest.raises(FrozenInstanceError):
        tablero.grid = esperado


@pytest.mark.parametrize("variante", [None, 15, "#" * 31, [], ["#" * 31] * 30,
                                       ["#" * 30] * 31, [None] * 31,
                                       [["#"] * 31] * 31])
def test_rechaza_forma_invalida(variante):
    from laberinto import Laberinto
    with pytest.raises(ValueError):
        Laberinto(variante)


@pytest.mark.parametrize("caracter", ["x", "\t", "\n"])
def test_rechaza_caracter_ajeno(grid, cambiar, caracter):
    from laberinto import Laberinto
    with pytest.raises(ValueError):
        Laberinto(cambiar(grid, 1, 1, caracter))


def test_rechaza_centro_bloqueado(grid, cambiar):
    from laberinto import Laberinto
    with pytest.raises(ValueError):
        Laberinto(cambiar(grid, 1, 1, "#"))


def test_importacion_solo_biblioteca_estandar():
    resultado = subprocess.run(
        [sys.executable, "-S", "-c",
         "import laberinto, sys; assert 'pygame' not in sys.modules"],
        capture_output=True, text=True, check=False,
    )
    assert resultado.returncode == 0, resultado.stderr


@pytest.mark.parametrize("variante", ["ciclo", "desconexion", "desconexion_con224"])
def test_rechaza_grafo_invalido(variantes_grafo, variante):
    from laberinto import Laberinto
    with pytest.raises(ValueError):
        Laberinto(variantes_grafo[variante])


def test_acepta_los_cinco_tableros(registros):
    from laberinto import Laberinto
    for registro in registros:
        assert Laberinto(registro["grid"]).grid == tuple(registro["grid"])


CONTORNO = [(f, c) for f in range(31) for c in range(31)
            if f in (0, 30) or c in (0, 30)]


@pytest.mark.parametrize("fila,columna", CONTORNO)
def test_contorno_exacto(grid, cambiar, fila, columna):
    from laberinto import Laberinto
    alterado = "#" if (fila, columna) in ((1, 0), (29, 30)) else " "
    with pytest.raises(ValueError):
        Laberinto(cambiar(grid, fila, columna, alterado))


def test_metadatos_conservados_sin_referencias_compartidas(registros):
    from laberinto import EntradaCatalogo, Laberinto
    original = deepcopy(registros[0])
    original["extra"] = {"lista": [1, 2]}
    esperado = deepcopy(original)
    entrada = EntradaCatalogo(Laberinto(original["grid"]), original)
    original["extra"]["lista"].append(3)
    original["grid"][1] = "#" * 31
    anterior = entrada.datos
    assert anterior == esperado
    copia = entrada.datos
    copia["entrada"][0] = 999
    copia["extra"]["lista"].clear()
    copia["grid"].clear()
    assert entrada.datos == anterior == esperado
    assert entrada.laberinto.grid == tuple(esperado["grid"])


def test_metadatos_sin_obligaciones_nuevas(grid):
    from laberinto import EntradaCatalogo, Laberinto
    datos = {"grid": grid, "campo_libre": [None, {"x": 42}]}
    entrada = EntradaCatalogo(Laberinto(grid), datos)
    assert entrada.datos == datos
    assert "id" not in entrada.datos


def test_coordenadas_del_registro_no_son_casillas(registros):
    from laberinto import EntradaCatalogo, Laberinto
    for registro in registros:
        entrada = EntradaCatalogo(Laberinto(registro["grid"]), registro)
        assert entrada.datos["entrada"] == [1, 0]
        assert entrada.datos["salida"] == [29, 30]


def test_carga_cinco_y_preserva_archivo(registros):
    from pathlib import Path
    from laberinto import cargar_catalogo
    ruta = Path(__file__).resolve().parents[1] / "base" / "laberintos.json"
    original = ruta.read_bytes()
    resultado = cargar_catalogo(ruta)
    assert isinstance(resultado.entradas, tuple)
    assert len(resultado.entradas) == 5
    assert resultado.rechazadas == 0
    assert resultado.aviso is None
    assert [e.datos for e in resultado.entradas] == registros
    assert all(len(e.laberinto.grid) == 31 for e in resultado.entradas)
    assert ruta.read_bytes() == original


@pytest.mark.parametrize("invalida", [None, 3, [], {}, {"grid": None},
                                      {"grid": ["#"]}, {"grid": [1] * 31}])
def test_carga_parcial_conserva_orden(registros, escribir_catalogo, invalida):
    from laberinto import cargar_catalogo
    validas = [registros[4], registros[1], registros[4]]
    resultado = cargar_catalogo(str(escribir_catalogo([validas[0], invalida, *validas[1:]])))
    assert [e.datos for e in resultado.entradas] == validas
    assert resultado.rechazadas == 1
    assert resultado.aviso is None


@pytest.mark.parametrize("contenido,rechazadas", [([], 0), ([None, {}], 2)])
def test_catalogo_sin_validas(contenido, rechazadas, escribir_catalogo):
    from laberinto import cargar_catalogo
    resultado = cargar_catalogo(escribir_catalogo(contenido))
    assert resultado.entradas == ()
    assert resultado.rechazadas == rechazadas
    assert resultado.aviso == "No hay entradas válidas."


@pytest.mark.parametrize("contenido", [{}, None, 15, "lista"])
def test_catalogo_estructura_superior(contenido, escribir_catalogo):
    from laberinto import cargar_catalogo
    resultado = cargar_catalogo(escribir_catalogo(contenido))
    assert resultado.entradas == ()
    assert resultado.rechazadas == 0
    assert resultado.aviso == "El catálogo debe ser una lista."


@pytest.mark.parametrize("contenido", [b"", b"{", b"\xff\xfe"])
def test_archivo_no_interpretable(tmp_path, contenido):
    from laberinto import cargar_catalogo
    ruta = tmp_path / "laberintos.json"
    ruta.write_bytes(contenido)
    resultado = cargar_catalogo(ruta)
    assert resultado.entradas == ()
    assert resultado.rechazadas == 0
    assert resultado.aviso == "No se pudo leer el catálogo."


def test_archivo_inexistente(tmp_path):
    from laberinto import cargar_catalogo
    resultado = cargar_catalogo(tmp_path / "ausente.json")
    assert resultado.entradas == ()
    assert resultado.rechazadas == 0
    assert resultado.aviso == "No se pudo leer el catálogo."


def test_error_lectura_controlado(monkeypatch, tmp_path):
    from pathlib import Path
    from laberinto import cargar_catalogo
    def fallar(*argumentos, **opciones):
        raise PermissionError("Lectura denegada de prueba")
    monkeypatch.setattr(Path, "read_text", fallar)
    resultado = cargar_catalogo(tmp_path / "protegido.json")
    assert resultado.entradas == ()
    assert resultado.rechazadas == 0
    assert resultado.aviso == "No se pudo leer el catálogo."


def test_no_oculta_errores_inesperados(monkeypatch, tmp_path):
    from pathlib import Path
    from laberinto import cargar_catalogo
    def fallar(*argumentos, **opciones):
        raise RuntimeError("Defecto inesperado de prueba")
    monkeypatch.setattr(Path, "read_text", fallar)
    with pytest.raises(RuntimeError):
        cargar_catalogo(tmp_path / "archivo.json")


def test_catalogo_solo_exige_grid(grid, escribir_catalogo):
    from laberinto import cargar_catalogo
    registro = {"grid": grid}
    resultado = cargar_catalogo(escribir_catalogo([registro]))
    assert len(resultado.entradas) == 1
    assert resultado.entradas[0].datos == registro
    assert resultado.aviso is None


INVALIDAS = [None, 1, (), (0,), (0, 0, 0), [0, 0], (True, 0), (0, False),
             (1.0, 0), (0, "1"), (-1, 0), (0, -1), (15, 0), (0, 15)]


def test_paredes_validas_antes_de_implementacion(grid):
    from laberinto import Laberinto
    tablero = Laberinto(grid)
    resultados = set()
    for fila in range(15):
        for columna in range(14):
            esperado = grid[2 * fila + 1][2 * columna + 2] == "#"
            assert tablero.hay_pared((columna, fila), (columna + 1, fila)) is esperado
            resultados.add(esperado)
    assert resultados == {False, True}


@pytest.mark.parametrize("invalida", INVALIDAS)
@pytest.mark.parametrize("lado", ["origen", "destino"])
def test_pared_rechazo_sin_mutacion(registros, invalida, lado):
    from laberinto import EntradaCatalogo, Laberinto
    entrada = EntradaCatalogo(Laberinto(registros[0]["grid"]), registros[0])
    tablero = entrada.laberinto
    original, datos = tablero.grid, entrada.datos
    anterior = tablero.hay_pared((0, 0), (1, 0))
    origen, destino = (invalida, (1, 0)) if lado == "origen" else ((0, 0), invalida)
    with pytest.raises(ValueError):
        tablero.hay_pared(origen, destino)
    assert tablero.grid == original
    assert entrada.datos == datos
    assert tablero.hay_pared((0, 0), (1, 0)) is anterior


@pytest.mark.parametrize("destino", [(0, 0), (1, 1), (2, 0), (0, 2)])
def test_pared_exige_adyacencia(grid, destino):
    from laberinto import Laberinto
    tablero = Laberinto(grid)
    original = tablero.grid
    anterior = tablero.hay_pared((0, 0), (1, 0))
    with pytest.raises(ValueError):
        tablero.hay_pared((0, 0), destino)
    assert tablero.grid == original
    assert tablero.hay_pared((0, 0), (1, 0)) is anterior


def test_vecinos_y_simetria_exhaustivos(registros):
    from laberinto import Laberinto
    for registro in registros:
        g = registro["grid"]
        tablero = Laberinto(g)
        for f in range(15):
            for c in range(15):
                esperados = []
                for nc, nf in ((c, f - 1), (c + 1, f), (c, f + 1), (c - 1, f)):
                    if 0 <= nc < 15 and 0 <= nf < 15:
                        pared = g[f + nf + 1][c + nc + 1] == "#"
                        assert tablero.hay_pared((c, f), (nc, nf)) is pared
                        assert tablero.hay_pared((nc, nf), (c, f)) is pared
                        if not pared:
                            esperados.append((nc, nf))
                assert tablero.vecinos_accesibles((c, f)) == esperados


def test_vecinos_entrada_laberinto_uno(grid):
    from laberinto import Laberinto
    assert grid[1][2] == " "
    assert grid[2][1] == "#"
    assert Laberinto(grid).vecinos_accesibles((0, 0)) == [(1, 0)]


@pytest.mark.parametrize("invalida", INVALIDAS)
def test_vecinos_rechazo_sin_mutacion(registros, invalida):
    from laberinto import EntradaCatalogo, Laberinto
    entrada = EntradaCatalogo(Laberinto(registros[0]["grid"]), registros[0])
    tablero = entrada.laberinto
    grid_anterior, datos = tablero.grid, entrada.datos
    anterior = tablero.vecinos_accesibles((0, 0))
    esperado = anterior.copy()
    with pytest.raises(ValueError):
        tablero.vecinos_accesibles(invalida)
    assert tablero.grid == grid_anterior
    assert entrada.datos == datos
    assert anterior == esperado
    assert tablero.vecinos_accesibles((0, 0)) == esperado


def test_vecinos_resultados_independientes(registros):
    from laberinto import EntradaCatalogo, Laberinto
    entrada = EntradaCatalogo(Laberinto(registros[0]["grid"]), registros[0])
    tablero = entrada.laberinto
    original, datos = tablero.grid, entrada.datos
    anterior = tablero.vecinos_accesibles((0, 0))
    copia = tablero.vecinos_accesibles((0, 0))
    assert copia is not anterior
    copia.clear()
    copia.append((99, 99))
    assert anterior == [(1, 0)]
    assert tablero.vecinos_accesibles((0, 0)) == anterior
    assert tablero.grid == original
    assert entrada.datos == datos


@pytest.mark.parametrize("indice", range(5))
def test_distancias_todos_los_origenes(registros, distancias_referencia, indice):
    from laberinto import Laberinto
    g = registros[indice]["grid"]
    tablero = Laberinto(g)
    for fila in range(15):
        for columna in range(15):
            origen = (columna, fila)
            esperadas = distancias_referencia(g, origen)
            resultado = tablero.distancias_desde(origen)
            assert len(resultado) == 225
            assert resultado[origen] == 0
            assert resultado == esperadas
            assert tablero.distancias_desde(origen) == resultado


def test_distancias_serpiente_con_rodeos(serpiente):
    from laberinto import Laberinto
    g, posiciones = serpiente
    tablero = Laberinto(g)
    for indice in (0, 14, 15, 112, 224):
        distancias = tablero.distancias_desde(posiciones[indice])
        assert distancias == {casilla: abs(i - indice)
                              for i, casilla in enumerate(posiciones)}
    assert tablero.distancias_desde((0, 0))[(14, 14)] == 224
    assert tablero.distancias_desde((0, 0))[(0, 1)] == 29


@pytest.mark.parametrize("invalida", INVALIDAS)
def test_distancias_rechazo_sin_mutacion(registros, invalida):
    from laberinto import EntradaCatalogo, Laberinto
    entrada = EntradaCatalogo(Laberinto(registros[0]["grid"]), registros[0])
    tablero = entrada.laberinto
    original, datos = tablero.grid, entrada.datos
    anterior = tablero.distancias_desde((0, 0))
    esperado = anterior.copy()
    with pytest.raises(ValueError):
        tablero.distancias_desde(invalida)
    assert tablero.grid == original
    assert entrada.datos == datos
    assert anterior == esperado
    assert tablero.distancias_desde((0, 0)) == esperado


def test_distancias_resultados_independientes(registros):
    from laberinto import EntradaCatalogo, Laberinto
    entrada = EntradaCatalogo(Laberinto(registros[0]["grid"]), registros[0])
    tablero = entrada.laberinto
    original, datos = tablero.grid, entrada.datos
    anterior = tablero.distancias_desde((0, 0))
    esperado = anterior.copy()
    copia = tablero.distancias_desde((0, 0))
    assert copia is not anterior
    copia.clear()
    otro_origen = tablero.distancias_desde((14, 14))
    assert otro_origen[(14, 14)] == 0
    otro_origen[(0, 0)] = -1
    assert anterior == esperado
    assert tablero.distancias_desde((0, 0)) == esperado
    assert tablero.distancias_desde((14, 14))[(0, 0)] == esperado[(14, 14)]
    assert tablero.grid == original
    assert entrada.datos == datos
