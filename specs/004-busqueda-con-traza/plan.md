# Plan de implementación: Encontrar caminos y explicar el backtracking

**Funcionalidad**: 004-busqueda-con-traza | **Fecha**: 2026-10-23
**Especificación**: [spec.md](spec.md) | **Fuente**: [SPEC-LAB-001 §7](../../base/SPEC.md)

## Resumen

Crear `fantasma_ia.py` con dos funciones: `buscar_camino_con_traza` y `buscar_camino`.
La búsqueda es en profundidad con una lista usada como pila y un conjunto de visitados.
Cada paso agrega un evento a la traza. No usa pygame ni azar.

## Contexto técnico

- **Lenguaje**: Python 3.10+.
- **Dependencias**: ninguna externa. Solo `laberinto.py` y la biblioteca estándar.
- **Pruebas**: pytest y pytest-cov de `requirements-dev.txt`.
- **Datos de prueba**: los 5 laberintos de `base/laberintos.json` mediante `tests/conftest.py`.
- **Escala**: 225 casillas, pila de 225 como máximo.
- **Rendimiento**: menos de 10 ms por búsqueda en 15×15 (RNF-4).

## Revisión de la constitución

| Principio | Cumplimiento |
|---|---|
| I. Lógica sin pygame | `fantasma_ia.py` no importa pygame |
| II. Pruebas primero | `tests/test_fantasma_ia.py` se escribe y falla antes del código |
| III. Cobertura 80 % | Se mide `--cov=fantasma_ia` aparte |
| IV. Dependencia única | No se agregan paquetes |
| V. Español | Nombres y mensajes en español |
| VI. Lo más simple | Dos funciones, una tupla con nombre, sin clases extra |
| VII. Terminado | Solo al pasar CA-03, 04, 05, 17, 18, 19, 20 y CA-27 literal |

## Diseño

### Evento

```python
class Evento(NamedTuple):
    tipo: str        # "apilar", "desapilar" o "encontrado"
    casilla: tuple   # (col, fila)
    pila: tuple      # copia de la pila después del evento, de base a cima
```

Se usa `NamedTuple` porque la fuente lo fija en §7.2 y es inmutable.

### Algoritmo

Sigue el pseudocódigo de §7.3 tal cual:

1. `pila = [origen]`, `visitados = {origen}`, evento `apilar(origen)`.
2. Mientras la pila tenga casillas, mirar la cima.
3. Si la cima es el destino: evento `encontrado(destino)` y devolver `pila[1:]`.
4. Buscar el primer vecino de `laberinto.vecinos_accesibles(cima)` que no esté en visitados.
   Ese método ya respeta el orden arriba, derecha, abajo, izquierda.
5. Si hay vecino: apilarlo, marcarlo y registrar `apilar`.
6. Si no: sacar la cima y registrar `desapilar`.
7. Si la pila queda vacía: `ValueError("No existe camino.")`.

`buscar_camino` llama a la anterior y devuelve solo el camino.

### Casos límite

- Origen igual a destino: camino `[]`, traza `apilar(origen)`, `encontrado(origen)`.
- Destino desconectado: se prueba con un doble mínimo del laberinto que tenga
  `vecinos_accesibles`, porque `Laberinto` rechaza tableros desconectados.
- Varios retrocesos: los 5 laberintos reales tienen ramas sin salida.

## Archivos

```text
fantasma_ia.py              # nuevo
tests/test_fantasma_ia.py   # nuevo
specs/004-busqueda-con-traza/validacion.md   # evidencia de pruebas y cobertura
```

## Relación con otras specs

- Cierra CA-27 literal pendiente en 001: `distancias_desde(c)[x] == len(buscar_camino(c, x))`.
- 005 llamará a `buscar_camino` en cada turno del fantasma.
- 006 y 007 consumirán la traza; este módulo no anima ni dibuja.
