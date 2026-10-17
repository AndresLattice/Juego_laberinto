"""Modelo y consultas de laberintos, independientes de la interfaz gráfica."""

from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
import json
from pathlib import Path

Casilla = tuple[int, int]


@dataclass(frozen=True)
class Laberinto:
    """Tablero validado con filas inmutables."""

    grid: tuple[str, ...]

    def __post_init__(self):
        if not isinstance(self.grid, (list, tuple)) or len(self.grid) != 31:
            raise ValueError("El tablero debe tener 31 filas.")
        if any(not isinstance(fila, str) or len(fila) != 31 for fila in self.grid):
            raise ValueError("Cada fila debe tener 31 caracteres.")
        filas = tuple(self.grid)
        if any(caracter not in "# " for fila in filas for caracter in fila):
            raise ValueError("El tablero solo admite paredes y espacios.")
        if any(filas[fila][columna] != " "
               for fila in range(1, 30, 2) for columna in range(1, 30, 2)):
            raise ValueError("Todas las casillas deben ser transitables.")
        for fila in range(31):
            for columna in range(31):
                if fila in (0, 30) or columna in (0, 30):
                    esperado = " " if (fila, columna) in ((1, 0), (29, 30)) else "#"
                    if filas[fila][columna] != esperado:
                        raise ValueError("El contorno solo admite la entrada y la salida.")
        object.__setattr__(self, "grid", filas)
        conexiones = sum(
            1 for fila in range(15) for columna in range(15)
            for vecino in self._vecinos((columna, fila))
            if vecino > (columna, fila)
        )
        if conexiones != 224:
            raise ValueError("El laberinto debe tener 224 conexiones internas.")
        pendientes = [(0, 0)]
        visitadas = {(0, 0)}
        while pendientes:
            for vecino in self._vecinos(pendientes.pop()):
                if vecino not in visitadas:
                    visitadas.add(vecino)
                    pendientes.append(vecino)
        if len(visitadas) != 225:
            raise ValueError("Todas las casillas deben estar conectadas.")

    @staticmethod
    def _validar_casilla(casilla):
        if (not isinstance(casilla, tuple) or len(casilla) != 2
                or any(not isinstance(valor, int) or isinstance(valor, bool)
                       or not 0 <= valor < 15 for valor in casilla)):
            raise ValueError("La casilla debe contener columna y fila enteras entre 0 y 14.")

    def hay_pared(self, origen: Casilla, destino: Casilla) -> bool:
        """Consultar el separador entre dos casillas ortogonalmente adyacentes."""
        self._validar_casilla(origen)
        self._validar_casilla(destino)
        c1, f1 = origen
        c2, f2 = destino
        if abs(c1 - c2) + abs(f1 - f2) != 1:
            raise ValueError("Las casillas deben ser vecinas ortogonales distintas.")
        return self.grid[f1 + f2 + 1][c1 + c2 + 1] == "#"

    def vecinos_accesibles(self, casilla: Casilla) -> list[Casilla]:
        """Devolver vecinos transitables en orden arriba, derecha, abajo, izquierda."""
        self._validar_casilla(casilla)
        return list(self._vecinos(casilla))

    def distancias_desde(self, origen: Casilla) -> dict[Casilla, int]:
        """Contar pasos permitidos desde el origen hasta todas las casillas."""
        self._validar_casilla(origen)
        distancias = {origen: 0}
        pendientes = deque([origen])
        while pendientes:
            actual = pendientes.popleft()
            for vecino in self._vecinos(actual):
                if vecino not in distancias:
                    distancias[vecino] = distancias[actual] + 1
                    pendientes.append(vecino)
        return distancias

    def _vecinos(self, casilla):
        columna, fila = casilla
        for dc, df in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            c, f = columna + dc, fila + df
            if 0 <= c < 15 and 0 <= f < 15:
                if self.grid[fila + f + 1][columna + c + 1] == " ":
                    yield (c, f)


@dataclass(frozen=True, init=False)
class EntradaCatalogo:
    """Laberinto y datos originales con copias aisladas para el consumidor."""

    laberinto: Laberinto
    _datos: dict = field(repr=False)

    def __init__(self, laberinto: Laberinto, datos: dict):
        object.__setattr__(self, "laberinto", laberinto)
        object.__setattr__(self, "_datos", deepcopy(datos))

    @property
    def datos(self) -> dict:
        return deepcopy(self._datos)


@dataclass(frozen=True)
class ResultadoCarga:
    """Entradas aceptadas y diagnóstico de disponibilidad del catálogo."""

    entradas: tuple[EntradaCatalogo, ...]
    rechazadas: int
    aviso: str | None


def cargar_catalogo(ruta: str | Path) -> ResultadoCarga:
    """Leer el catálogo sin descartar sus entradas válidas ni modificar la fuente."""
    try:
        registros = json.loads(Path(ruta).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ResultadoCarga((), 0, "No se pudo leer el catálogo.")
    if not isinstance(registros, list):
        return ResultadoCarga((), 0, "El catálogo debe ser una lista.")
    entradas = []
    rechazadas = 0
    for registro in registros:
        if not isinstance(registro, dict):
            rechazadas += 1
            continue
        try:
            tablero = Laberinto(registro.get("grid"))
        except ValueError:
            rechazadas += 1
            continue
        entradas.append(EntradaCatalogo(tablero, registro))
    aviso = None if entradas else "No hay entradas válidas."
    return ResultadoCarga(tuple(entradas), rechazadas, aviso)
