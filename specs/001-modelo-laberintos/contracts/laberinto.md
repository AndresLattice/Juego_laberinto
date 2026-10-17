# Contrato público de laberinto.py

Contrato de biblioteca local para los consumidores del juego; no se exponen HTTP ni CLI.
Todas las operaciones son independientes de pygame y de la pantalla.

## Tipos y firmas previstas

```python
Casilla = tuple[int, int]

Laberinto(grid: tuple[str, ...])
Laberinto.vecinos_accesibles(casilla: Casilla) -> list[Casilla]
Laberinto.hay_pared(origen: Casilla, destino: Casilla) -> bool
Laberinto.distancias_desde(origen: Casilla) -> dict[Casilla, int]

EntradaCatalogo(laberinto: Laberinto, datos: dict)
EntradaCatalogo.datos  # propiedad: copia profunda nueva del registro

ResultadoCarga(entradas: tuple[EntradaCatalogo, ...], rechazadas: int, aviso: str | None)
cargar_catalogo(ruta: str | Path) -> ResultadoCarga
```

Las firmas describen interfaces, no cuerpos de implementación. La construcción de Laberinto
acepta también la lista de filas del archivo y la normaliza a tupla antes de exponerla.

## Precondiciones y errores

- Laberinto rechaza con ValueError los tableros inválidos según RF-03, con mensaje español.
- Una Casilla es una tupla de dos enteros no booleanos en 0..14. Forma, tipo o rango
  incorrectos en una consulta producen ValueError. No se usan índices negativos de Python.
- hay_pared requiere dos casillas ortogonalmente adyacentes; igualdad, diagonal o distancia
  mayor que uno producen ValueError. True indica pared; False conexión abierta.
- cargar_catalogo controla OSError, UnicodeError, errores de JSON y validación esperada;
  entrega resultado sin entradas y aviso si no hay catálogo utilizable.
- Una entrada que no sea un diccionario o cuyo grid sea inválido se cuenta como rechazada.
  La aceptación no añade reglas de unicidad ni requisitos a metadatos descriptivos.
- Los textos de aviso se presentan en español; el consumidor debe decidir por entradas y
  aviso, sin analizar frases para deducir el modo de respaldo.

## Garantías de consultas

Orden fijo de vecinos: arriba, derecha, abajo, izquierda. Solo casillas interiores al dominio;
las aperturas no generan vecinos exteriores. Simetría de hay_pared. Distancias mínimas de
pasos transitables, origen cero y todas las 225 casillas alcanzadas. Cada consulta devuelve
contenedores nuevos sin referencias mutables compartidas con otros resultados.

## Uso previsto por consumidores

- 002 consume entradas disponibles o aplica generación si el resultado no es utilizable;
  generación y selección no se añaden a este contrato de 001.
- 004 consume vecinos_accesibles y produce su propio camino/traza.
- 005 consume distancias_desde y hay_pared; aparición y movimientos siguen fuera de 001.
- 007 lee grid para representar el tablero sin modificarlo.
- 008 transforma aviso en el mensaje de respaldo exigido por la especificación global.

CA-27 se verifica ahora con un oráculo independiente; al integrar 004 se compara literalmente
cada distancia con la longitud de buscar_camino, sin crear esa función en 001.
