# Modelo de datos: laberintos

## Casilla

Tupla (columna, fila) de dos enteros, excluyendo booleanos, cada uno entre 0 y 14.
Entrada lógica: (0,0); meta lógica: (14,14). Consultas fuera del dominio: ValueError.

## Laberinto

- grid: tupla de 31 cadenas de longitud 31; copia del tablero recibido.
- Valor inmutable; constructor valida y normaliza una secuencia de filas.
- Centro de (c,f): grid[2*f+1][2*c+1]. Separador de casillas adyacentes A y B:
  grid[fA+fB+1][cA+cB+1].
- Solo # y espacio. Centros transitables. Contorno abierto solo en (fila=1,columna=0)
  y (fila=29,columna=30). Los demás puntos del contorno son #, incluidas esquinas.
- Exactamente 224 conexiones internas y 225 casillas conectadas. Sin ciclo ni desconexión.
- No tiene actores, modo de selección, semilla, cache mutable ni estado gráfico.

## EntradaCatalogo

Relaciona un Laberinto validado con una copia profunda del registro fuente.
La propiedad datos devuelve una copia profunda nueva, incluido el grid original como lista.
Preserva id, tipo, descripcion, entrada, salida y cualquier otro dato presente, sin inventar
valores ausentes ni añadir validaciones de metadatos no exigidas. No deduplica identidades.
Las coordenadas entrada/salida del registro son referencias del grid; no sustituyen las
coordenadas lógicas del tablero. El consumidor usa el Laberinto para reglas de movimiento.

## ResultadoCarga

- entradas: tupla de EntradaCatalogo, en el orden original de las aceptadas.
- rechazadas: cantidad de entradas individuales inválidas; cero si no se pudo leer la lista.
- aviso: texto español o None; indica catálogo no utilizable cuando entradas está vacía.

Estados observables de carga:

| Situación | entradas | rechazadas | aviso |
|---|---|---|---|
| Lista válida completa | Todas las válidas | 0 | None |
| Lista mixta | Solo válidas | Número inválido | None |
| Lista sin válidas | Vacía | Número inválido | No hay entradas válidas |
| Lista vacía | Vacía | 0 | No hay entradas válidas |
| Archivo inaccesible o contenido inválido | Vacía | 0 | No se pudo leer el catálogo |
| Estructura superior no es lista | Vacía | 0 | El catálogo debe ser una lista |

La carga no escribe archivos, no lanza cierre del programa y no decide el respaldo.
Un fallo inesperado del programa no se convierte silenciosamente en un aviso de archivo.

## Resultados de consultas

- vecinos_accesibles: lista nueva de Casilla, en orden arriba/derecha/abajo/izquierda.
- hay_pared: booleano para un par adyacente válido; simétrico.
- distancias_desde: diccionario nuevo Casilla → entero no negativo, de 225 entradas;
  origen cero. Modificarlo no altera el Laberinto ni consultas anteriores.

No existen transiciones persistentes del modelo: las operaciones son consultas. Crear el
valor pasa de datos no confiables a objeto validado, o termina con error de validación.
